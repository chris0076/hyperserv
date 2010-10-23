"""This file handles the events that happen ingame"""

import sbserver

from hyperserv.events import eventHandler, policyHandler, triggerServerEvent, registerPolicyEventHandler

from hypershade.cubescript import checkforCS, playerCS, systemCS
from hypershade.usersession import UserSessionManager

from hyperserv.notices import serverNotice

from hypershade.config import config
from hypershade.bandatabase import bandatabase

from hypershade.util import formatCaller, ipLongToString

#process cubescript
registerPolicyEventHandler('allow_message', lambda cn, msg: checkforCS(("ingame",cn),msg)==0)

systemCS.executestring("map %s %s" % (config["defaultmap"],config["defaultmode"]))
systemCS.executestring("mastermode %s" % config["defaultmastermode"])

@eventHandler('no_clients')
def noclients():
	serverNotice("Server is now empty.")
	systemCS.executestring("mastermode %s" % (config["defaultmastermode"]))

@eventHandler('player_message')
def PlayerMessage(cn,msg):
	triggerServerEvent("user_communication",[("ingame",cn),msg])

@eventHandler('echo')
def echoingame(caller,msg):
	if caller[0]=="ingame":
		sbserver.playerMessage(caller[1],"\f4%s" % msg)

@eventHandler('say')
def sayingame(msg):
	sbserver.message("\f4%s" % msg)

@eventHandler('user_communication')
def usercommunicationingame(caller,msg):
	if caller[0]=="ingame":
		return
	sbserver.message("\f2%s: \f0%s" % (formatCaller(caller),msg))
	
@eventHandler('notice')
def noticeingame(msg):
	sbserver.message("\f1%s" % msg)

#User Sessions
@eventHandler('player_connect')
def playerconnect(cn):
	UserSessionManager.create(("ingame",cn))
	
@eventHandler('player_disconnect')
def playerdisconnect(cn):
	UserSessionManager.destroy(("ingame",cn))

#Connection denied handling
@policyHandler('check_connect_password')
def checkConnectPassword(cn,password):
	return False
	#TODO: see http://github.com/SirAlex/hyperserv/issues#issue/23

@policyHandler('check_connect_banned')
def checkConnectBanned(cn):
	checklist=(
		sbserver.playerName(cn),
		ipLongToString(sbserver.playerIpLong(cn))
	)
	
	matches=bandatabase.search(checklist)
	
	if len(matches)>0:
		timeperiod="indefinatelly"
		reason=matches[0][2]
		if reason== "":
			reason="none"
		serverNotice("%s is banned %s, reason: %s" % (sbserver.playerName(cn),matches[0][1],reason))
		return True
	
	return False

@eventHandler('vote_map')
def voteMap(caller,mode,name):
	otherplayers=[(session,user) for session,user in UserSessionManager.items() if session[0]=='ingame' and session!=caller]
	if len(otherplayers)==0:
		sbserver.setMap(name,mode)
