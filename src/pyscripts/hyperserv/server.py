"""This file contains all the basic commands that the server needs to be playable, this does not handle '/' type requests from clients only server-side cubescript commands"""
from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from hyperserv.cubescript import systemCS
from hyperserv.permissions import masterRequired, adminRequired, trustedRequired
from hyperserv.util import ipLongToString, formatOwner, modeNumber

def whoami(caller):
	return str(caller.owner)
systemCS.addfunction("whoami",whoami)

@masterRequired
def changeMap(caller,name,mode="coop"):
	return sbserver.setMap(name,modeNumber(mode))
systemCS.addfunction("map",changeMap)

@masterRequired
def setMaster(caller):
	if(caller[0]=="ingame"):
		return sbserver.setMaster(caller[1])
	return
systemCS.addfunction("master",setMaster)

@adminRequired
def setAdmin(caller):
	if(caller[0]=="ingame"):
		return sbserver.setAdmin(caller[1])
	return
systemCS.addfunction("admin",setAdmin)

def who(caller,where="ingame"):
	if where=="ingame":
		def cndetails(cn):
			return sbserver.playerName(cn)+" (cn"+str(cn)+"/"+ipLongToString(sbserver.playerIpLong(cn))+")"
		return '; '.join(map(cndetails,sbserver.clients()))
systemCS.addfunction("who",who)

def listCommands(caller):
	commands=systemCS.functions.keys()
	commands.sort()
	return ' '.join(commands)
systemCS.addfunction("list",listCommands)

@trustedRequired
def say(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("say",[string])
	sbserver.message(string)
	return string
systemCS.addfunction("say",say)

def echo(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("echo",[caller.owner,string])
	if caller.owner[0]=="ingame":
		sbserver.playerMessage(caller.owner[1],string)
systemCS.addfunction("echo",echo)

@eventHandler('user_communication')
def usercommunicationingame(who,msg):
	if who[0]=="ingame":
		return
	sbserver.message(""+formatOwner(who)+": "+msg)