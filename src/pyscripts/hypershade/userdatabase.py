from hypershade.config import config

class UserDatabase():
	def __init__(self):
		if config["dbtype"]=="mysql":
			import MySQLdb
			
			mysqldb=MySQLdb.connect(host=config["dbhost"],user=config["dbuser"],passwd=config["dbpassword"],db=config["dbname"])
			self.cursor=mysqldb.cursor()
		else:
			raise Exception("Database driver %s not implemented." % config["dbtype"])
	
	def __iter__(self):
		for user in self.items():
			yield user[0]
	
	def items(self):
		self.cursor.execute('SELECT * FROM `users` where `key` = "privileges"')
		return self.cursor.fetchall()
	
	def __getitem__(self,username):
		self.cursor.execute('SELECT `user` FROM `users` WHERE `user` = "%s" AND `key` = "privileges"' % (username,))
		
		if self.cursor.rowcount==0:
			raise KeyError("No such user: %s" % username)
		
		return User(self.cursor,username)
	
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
	def __init__(self,cursor,username):
		self.cursor=cursor
		self.username=username
	
	def __iter__(self):
		for row in self.items():
			yield row[0]
	
	def items(self):
		self.cursor.execute('SELECT `key`,`value` FROM `users` WHERE `user` = "%s"' % (self.username))
		return (("username",self.username),)+self.cursor.fetchall()
	
	def __getitem__(self,key):
		self.cursor.execute('SELECT value FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
		return tuple(row[0] for row in self.cursor.fetchall())
	
	def __repr__(self):
		return repr(self.items())
	
	def __cmp__(self,other):
		return cmp(self.username,other.username)

userdatabase=UserDatabase()
