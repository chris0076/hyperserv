class PermissionError(Exception): pass

class UserSessionManagerClass(dict):
	def create(self,who,login=("notloggedin","")):
		self[who]=login
		return self[who]
	def destroy(self,who):
		return self.pop(who)
	def rename(self,who,to):
		self.create(to,self.destroy(who))
	def __missing__(self,key):
		return self.create(key)
	
	def checkPermissions(self,caller,level):
		if caller==("system",""): #allow system do do everything
			return
		
		session=self[caller]
		if level=="none" or level=="":
			return
		elif level=="master":
			if session[1] in ("master","trusted","admin"):
				return
		elif level=="trusted":
			if session[1] in ("trusted","admin"):
				return
		elif level=="admin":
			if session[1] in ("admin",):
				return
		else:
			raise PermissionError("Permission Level %s not recognized" % (level,))
		raise PermissionError("Permission denied, you need %s privileges." % (level,))
		
UserSessionManager=UserSessionManagerClass()