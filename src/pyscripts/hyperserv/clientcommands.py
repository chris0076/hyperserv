""" handle '/' type requests from clients and translate them into cubescript"""

import sbserver
from hyperserv.events import eventHandler
from hyperserv.servercommands import ServerError

from hypershade.cubescript import checkforCS, playerCS
from hypershade.usersession import UserSessionManager
from hypershade.userdatabase import userdatabase
from hypershade.usercommands import succeedLogin

@eventHandler("player_setmaster")
def clientSetMaster(caller,text):
	if text=="":
		simpleMasterRequest(("ingame",caller))
	else:
		checkforCS(("ingame",caller),"@login %s" % text)

@eventHandler("player_setmaster_off")
def clientLoseMaster(caller):
	checkforCS(("ingame",caller),"@relinquish;logout")

@eventHandler("player_request_spectate")
def clientSpectate(caller,who):
	checkforCS(("ingame",caller),"@spectator 1 %s" % who)

@eventHandler("player_request_unspectate")
def clientUnspectate(caller,who):
	checkforCS(("ingame",caller),"@spectator 0 %s" % who)

@eventHandler("player_map_vote")
def clientMapVote(caller,mapname,mode):
	checkforCS(("ingame",caller),"@map %s %s" % (mapname,mode))

@eventHandler("player_set_mastermode")
def clientMastermode(caller,mastermode):
	checkforCS(("ingame",caller),"@mastermode %s" % mastermode)

@eventHandler('player_auth_succeed')
def clientAuth(caller,name):
	authLogin(("ingame",caller),name)

@eventHandler("player_kick")
def clientKick(caller,who):
	#TODO: fix this kick event mess, both the notice and this
	print "kick",caller,who

##
#Auth and simple setmaster
def authLogin(caller,authname):
	user=userdatabase.search("auth name",authname)
	if user is not None:
		succeedLogin(caller,dict(user.items()))
	else:
		#normal auth request, not trying to login
		setSimpleMaster(caller)

def simpleMasterRequest(caller):
	#check for other privileged people
	privileged=[(session,user) for session,user in UserSessionManager.items() if session[0]=='ingame' and user[1]!='']
	
	if len(privileged)==0:
		setSimpleMaster(caller)
	else:
		playerCS.executeby(caller,"echo PermissionError: There are masters/admins present.")
		raise PermissionError("There are masters/admins present.")

def setSimpleMaster(caller):
	"""sets the caller a simple master, just like /setmaster 1 does it on a vanilla server"""
	UserSessionManager[caller]=("notloggedin","master")
	playerCS.executeby(caller,"master")