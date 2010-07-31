from hypershade.database import database

class UserDatabase():
	def __iter__(self):
		for user in self.items():
			yield user[0]
	
	def items(self):
		database.query('SELECT * FROM `users` where `key` = "privileges"')
		return tuple(database.cursor.fetchall())
	
	def __getitem__(self,username):
		database.query('SELECT `user` FROM `users` WHERE `user` = "%s" AND `key` = "privileges"' % (username))
		
		if database.cursor.rowcount==0:
			raise KeyError("No such user: %s" % (username))
		
		return User(username)
	
	def __setitem__(self,username,privileges):
		try:
			del self[username]["privileges"]
		except:
			pass
		User(username)["privileges"]=privileges
	
	def __delitem__(self,username):
		database.query('DELETE FROM `users` WHERE `user` = "%s"' % (username))
	
	def __repr__(self):
		return repr(self.items())
	
	def search(self,key,value):
		database.query('SELECT `user` FROM `users` WHERE `key` = "%s" and `value` = "%s"' % (key, value))
		result=database.cursor.fetchone()
		if result is not None:
			return self[result[0]]
		else:
			return None

class User():
	def __init__(self,username):
		self.username=username
	
	def __iter__(self):
		for row in self.items():
			yield row[0]
	
	def items(self):
		database.query('SELECT `key`,`value` FROM `users` WHERE `user` = "%s"' % (self.username))
		return (("username",self.username),)+tuple(database.cursor.fetchall())
	
	def __getitem__(self,key):
		database.query('SELECT value FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
		return tuple(row[0] for row in database.cursor.fetchall())
	
	def __setitem__(self,key,values):
		del self[key] #delete the old values
		if type(values) is str:
			#probably a mistake, just one value is wanted
			values=(values,)
		for value in values:
			database.query('INSERT INTO `users` VALUES ("%s","%s","%s")' % (self.username,key,value))
	
	def __delitem__(self, key):
		database.query('DELETE FROM `users` WHERE `user` = "%s" AND `key` = "%s"' % (self.username,key))
	
	def __repr__(self):
		return repr(self.items())
	
	def __cmp__(self,other):
		return cmp(self.username,other.username)

userdatabase=UserDatabase()
