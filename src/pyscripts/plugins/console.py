#!/usr/bin/env python

from urwidUI import urwidUI

#HyperServ
from hyperserv.events import eventHandler, triggerServerEvent
from hypershade.config import config
from hypershade.cubescript import checkforCS
from hypershade.usersession import UserSessionManager
from hypershade.util import formatCaller

ui=urwidUI()
user=("console",config["consoleuser"])
UserSessionManager[user]=(config["consoleuser"],"admin")

ui.firstLine='HyperServ, logged in as "%s' % (user,)

@eventHandler('echo')
def echoconsole(caller,msg):
	if caller==user:
		ui.addLine(msg)

@eventHandler('say')
def sayconsole(msg):
	ui.addLine(msg)

@eventHandler('user_communication')
def usercommunicationconsole(caller,msg):
	ui.addLine(formatCaller(caller)+": "+msg)

@eventHandler('notice')
def noticeconsole(msg):
	ui.addLine("Notice: "+msg)

def lineRecieved(text):
	if(checkforCS(user,text)==0):
		triggerServerEvent("user_communication",[user,text])
ui.lineRecievedCallback=lineRecieved