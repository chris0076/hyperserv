from hypershade.config import config

class UserDatabase():
	def __init__(self):
		if config["dbtype"]=="mysql":
			import MySQLdb
			self.connection=MySQLdb.connect(host=config["dbhost"],user=config["dbuser"],passwd=config["dbpassword"],db=config["dbname"])
		elif config["dbtype"]=="sqlite":
			import sqlite3
			self.connection = sqlite3.connect(config["dburl"])
			self.connection.text_factory = str
		else:
			raise Exception("Database driver %s not implemented." % config["dbtype"])
		self.cursor=self.connection.cursor()
	
	def __iter__(self):
		for user in self.items():
			yield user[0]
	
	def items(self):
		self.cursor.execute('SELECT * FROM `users` where `key` = "privileges"')
		return tuple(self.cursor.fetchall())
	
	def __getitem__(self,username):
		self.cursor.execute('SELECT `user` FROM `users` WHERE `user` = "%s" AND `key` = "privileges"' % (username))
		
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
		self.cursor.execute('DELETE FROM `users` WHERE `user` = "%s"' % (username))
		self.connection.commit()
	
	def __repr__(self):
		return repr(self.items())
	
	def search(self,key,value):
		self.cursor.execute('SELECT `user` FROM `users` WHERE `key` = "%s" and `value` = "%s"' % (key, value))
		result=self.cursor.fetchone()
		if result is not None:
			return self[result[0]]
		else:
			return None

class User():
	def __init__(self,parent,username):
		self.cursor=parent.cursor
		self.connection=parent.connection
		self.username=username
	
	def __iter__(self):
		for row in self.items():
			yield row[0]
	
	def items(self):
		self.cursor.execute('SELECT `key`,`value` FROM `users` WHERE `user` = "%s"' % (self.username))
		return (("username",self.username),)+tuple(self.cursor.fetchall())
	
	def __getitem__(self,key):
		self.cursor.execute('SELECT value FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
		return tuple(row[0] for row in self.cursor.fetchall())
	
	def __setitem__(self,key,values):
		del self[key] #delete the old values
		if type(values) is str:
			#probably a mistake, just one value is wanted
			values=(values,)
		for value in values:
			self.cursor.execute('INSERT INTO `users` VALUES ("%s","%s","%s")' % (self.username,key,value))
			self.connection.commit()
	
	def __delitem__(self, key):
		self.cursor.execute('DELETE FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
		self.connection.commit()
	
	def __repr__(self):
		return repr(self.items())
	
	def __cmp__(self,other):
		return cmp(self.username,other.username)

userdatabase=UserDatabase()
