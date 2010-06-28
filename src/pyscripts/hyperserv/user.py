#from hyperserv.events import eventHandler
import sbserver

from hyperserv.permissions import userSessions
from hyperserv.cubescript import CSCommand

class UserSessionManagerClass():
	def create(self,who,login=("notloggedin","")):
		userSessions[who]=login
	def destroy(self,who):
		if who in userSessions.keys():
			return userSessions.pop(who)
	def rename(self,who,to):
		self.create(to,self.destroy(who))
UserSessionManager=UserSessionManagerClass()

@CSCommand("login")
def login(caller):
	if caller[0]=="irc":
		username=caller[1].rstrip("_")
	if caller[0]=="ingame":
		username=sbserver.playerName(caller[1])
	userSessions[caller]=(username,"admin")
	
@CSCommand("whoami")
def whoami(caller,param=""):
	if param=="+login":
		return "%s - %s" % (str(caller),str(userSessions[caller]))
	return str(caller)

@CSCommand("listusersessions","admin")
def listusersessions(caller):
	return str(userSessions)