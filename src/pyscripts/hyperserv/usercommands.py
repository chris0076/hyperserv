#from hyperserv.events import eventHandler
from hyperserv.cubescript import CSCommand
from hyperserv.usersession import UserSessionManager
from hyperserv.notices import serverNotice

@CSCommand("login")
def login(caller):
	if caller[0]=="irc":
		username=caller[1].rstrip("_")
	if caller[0]=="ingame":
		username=sbserver.playerName(caller[1])
	serverNotice("%s has logged in from %s" % (username, caller[0]))
	UserSessionManager[caller]=(username,"admin")
	
@CSCommand("whoami")
def whoami(caller,param=""):
	if param=="+login":
		return "%s - %s" % (str(caller),str(UserSessionManager[caller]))
	return str(caller)

@CSCommand("listusersessions","admin")
def listusersessions(caller):
	return str(UserSessionManager)