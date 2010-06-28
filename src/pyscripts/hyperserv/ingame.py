"""This file handles the events that happen ingame"""
from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from hyperserv.cubescript import checkforCS
from hyperserv.util import formatOwner

@eventHandler('player_message')
def PlayerMessage(cn,msg):
	if checkforCS(("ingame",cn),msg)==0:
		triggerServerEvent("user_communication",[("ingame",cn),msg])

@eventHandler('echo')
def ingameecho(caller,msg):
	if caller[0]=="ingame":
		sbserver.playerMessage(caller[1],msg)

@eventHandler('say')
def sayirc(msg):
	sbserver.message(msg)

@eventHandler('user_communication')
def usercommunicationingame(caller,msg):
	if caller[0]=="ingame":
		return
	sbserver.message(""+formatOwner(caller)+": "+msg)
	
@eventHandler('notice')
def noticeirc(msg):
	sbserver.message(msg)