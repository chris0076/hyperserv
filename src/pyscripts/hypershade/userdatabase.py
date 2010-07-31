from hypershade.config import config


if config["dbtype"]=="mysql":
	import MySQLdb as sqlmodule
elif config["dbtype"]=="sqlite":
	import sqlite3 as sqlmodule
else:
	raise Exception("Database driver %s not implemented." % config["dbtype"])

class UserDatabase():
	def __init__(self):
		if config["dbtype"]=="mysql":
			self.connection=sqlmodule.connect(host=config["dbhost"],user=config["dbuser"],passwd=config["dbpassword"],db=config["dbname"])
		elif config["dbtype"]=="sqlite":
			self.connection = sqlmodule.connect(config["dburl"])
			self.connection.text_factory = str
		self.cursor=self.connection.cursor()
	
	def __iter__(self):
		for user in self.items():
			yield user[0]
	
	def items(self):
		self.query('SELECT * FROM `users` where `key` = "privileges"')
		return tuple(self.cursor.fetchall())
	
	def __getitem__(self,username):
		self.query('SELECT `user` FROM `users` WHERE `user` = "%s" AND `key` = "privileges"' % (username))
		
		if self.cursor.rowcount==0:
			raise KeyError("No such user: %s" % (username))
		
		return User(self,username)
	
	def __setitem__(self,username,privileges):
		try:
			del self[username]["privileges"]
		except:
			pass
		User(self,username)["privileges"]=privileges
	
	def __delitem__(self,username):
		self.query('DELETE FROM `users` WHERE `user` = "%s"' % (username))
	
	def __repr__(self):
		return repr(self.items())
	
	def search(self,key,value):
		self.query('SELECT `user` FROM `users` WHERE `key` = "%s" and `value` = "%s"' % (key, value))
		result=self.cursor.fetchone()
		if result is not None:
			return self[result[0]]
		else:
			return None
	
	def query(self,*args):
		try:
			self.cursor.execute(*args)
		except sqlmodule.OperationalError:
			self.__init__() #reconnect to the server
			self.cursor.execute(*args)
		self.connection.commit()

class User():
	def __init__(self,database,username):
		self.database=database
		self.username=username
	
	def __iter__(self):
		for row in self.items():
			yield row[0]
	
	def items(self):
		self.database.query('SELECT `key`,`value` FROM `users` WHERE `user` = "%s"' % (self.username))
		return (("username",self.username),)+tuple(self.database.cursor.fetchall())
	
	def __getitem__(self,key):
		self.database.query('SELECT value FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
		return tuple(row[0] for row in self.database.cursor.fetchall())
	
	def __setitem__(self,key,values):
		del self[key] #delete the old values
		if type(values) is str:
			#probably a mistake, just one value is wanted
			values=(values,)
		for value in values:
			self.database.query('INSERT INTO `users` VALUES ("%s","%s","%s")' % (self.username,key,value))
	
	def __delitem__(self, key):
		self.database.query('DELETE FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
	
	def __repr__(self):
		return repr(self.items())
	
	def __cmp__(self,other):
		return cmp(self.username,other.username)

userdatabase=UserDatabase()
