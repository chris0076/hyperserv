#from hyperserv.events import eventHandler
import sbserver

class PermissionError(Exception): pass

def checkPermissions(caller,level):
	if level=="none":
		pass
	elif level=="master":
		pass
	elif level=="trusted":
		pass
	elif level=="admin":
		pass
	else:
		raise PermissionError("Permission Level %s not recognized" % (format(level),))#
	return