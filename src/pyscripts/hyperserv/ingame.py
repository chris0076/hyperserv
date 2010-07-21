"""This file handles the events that happen ingame"""

import sbserver

from hyperserv.events import eventHandler, triggerServerEvent, registerPolicyEventHandler

from hypershade.cubescript import checkforCS
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
		sbserver.playerMessage(caller[1],msg)

@eventHandler('say')
def sayingame(msg):
	sbserver.message(msg)

@eventHandler('user_communication')
def usercommunicationingame(caller,msg):
	if caller[0]=="ingame":
		return
	sbserver.message(""+formatCaller(caller)+": "+msg)
	
@eventHandler('notice')
def noticeingame(msg):
	sbserver.message(msg)

#User Sessions
@eventHandler('player_connect')
def playerconnect(cn):
	UserSessionManager.create(("ingame",cn))
	
@eventHandler('player_disconnect')
def playerdisconnect(cn):
	UserSessionManager.destroy(("ingame",cn))