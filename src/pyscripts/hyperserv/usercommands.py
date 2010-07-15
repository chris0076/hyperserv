#from hyperserv.events import eventHandler
import sbserver

from hyperserv.cubescript import CSCommand

from hyperserv.usersession import UserSessionManager, PermissionError
from hyperserv.userdatabase import userdatabase

from hyperserv.notices import serverNotice

@CSCommand("login")
def login(caller,*params):
	if UserSessionManager[caller][0]!="notloggedin":
		logout(caller)
	
	#extract username and password
	username=None
	password=None
	if len(params)==2:
		username=params[0]
		password=params[1]
	elif len(params)==1:
		password=params[0]
	
	if username is None:
		if caller[0]=="irc":
			nickname=caller[1].rstrip("_")
			user=userdatabase.search("irc nick",nickname)
		elif caller[0]=="ingame":
			playername=sbserver.playerName(caller[1])
			user=userdatabase.search("sauerbraten name",playername)
		else:
			raise ValueError("Could not determine your login name.")
		if user is None:
			raise ValueError("Could not determine your login name.")
	else:
		user=userdatabase[username]
	
	#temporarly cache the user instance
	user=dict(user.items())
	
	if password is None:
		if caller[0]=="irc":
			#call an ident message, TODO
			pass
		if caller[0]=="ingame":
			#this can only be verified with auth, and that's user initiated
			pass
		else:
			#hostname based
			pass
	else:
		if user["password"]==password:
			succeed_login(caller,user)
			return
	
	raise PermissionError("Denied to login.")

def succeed_login(caller,user):
	serverNotice("%s has logged in from %s as %s" % (caller[1], caller[0], user["username"]))
	UserSessionManager[caller]=(user["username"],user["privileges"])

@CSCommand("logout")
def logout(caller):
	del UserSessionManager[caller]

@CSCommand("whoami")
def whoami(caller,param=""):
	if param=="+login":
		return "%s - %s" % (str(caller),str(UserSessionManager[caller]))
	return str(caller)

@CSCommand("listusersessions","admin")
def listusersessions(caller):
	return str(UserSessionManager)