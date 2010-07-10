"""This file handles the events that happen ingame"""

import sbserver
from hyperserv.events import eventHandler, triggerServerEvent
from hyperserv.cubescript import checkforCS

from hyperserv.permissions import UserSessionManager
from hyperserv.util import formatOwner

@eventHandler('player_message')
def PlayerMessage(cn,msg):
	if checkforCS(("ingame",cn),msg)==0:
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
	sbserver.message(""+formatOwner(caller)+": "+msg)
	
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