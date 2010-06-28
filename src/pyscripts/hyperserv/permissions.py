#from hyperserv.events import eventHandler
import sbserver

userSessions = {}

class PermissionError(Exception): pass

def checkPermissions(caller,level):
	try:
		if caller==("system",""): #allow system do do everything
			return
		
		session=userSessions[caller]
		if level=="none":
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
	except KeyError:
		userSessions[caller]=("notloggedin","")
		checkPermissions(caller,level)