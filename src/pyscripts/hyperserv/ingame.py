"""This file handles the events that happen ingame"""

import sbserver

from hyperserv.events import eventHandler, policyHandler, triggerServerEvent, registerPolicyEventHandler

from hypershade.cubescript import checkforCS, playerCS
from hypershade.usersession import UserSessionManager

from hypershade.util import formatCaller

#process cubescript
registerPolicyEventHandler('allow_message', lambda cn, msg: checkforCS(("ingame",cn),msg)==0)

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
	
@policyHandler('check_connect_banned')
def checkConnectBanned(cn):
	return False
