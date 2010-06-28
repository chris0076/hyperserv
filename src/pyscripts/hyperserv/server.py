"""This file contains all the basic commands that the server needs to be playable, this does not handle '/' type requests from clients only server-side cubescript commands"""
from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from hyperserv.cubescript import systemCS, CSCommand
from hyperserv.util import ipLongToString, formatOwner, modeNumber

@CSCommand("map","master")
def changeMap(caller,name,mode="coop"):
	return sbserver.setMap(name,modeNumber(mode))

@CSCommand("master","master")
def setMaster(caller):
	if(caller[0]=="ingame"):
		return sbserver.setMaster(caller[1])
	return

@CSCommand("admin","admin")
def setAdmin(caller):
	if(caller[0]=="ingame"):
		return sbserver.setAdmin(caller[1])
	return

@CSCommand("who")
def who(caller,where="ingame"):
	if where=="ingame":
		def cndetails(cn):
			return sbserver.playerName(cn)+" (cn"+str(cn)+"/"+ipLongToString(sbserver.playerIpLong(cn))+")"
		return '; '.join(map(cndetails,sbserver.clients()))

@CSCommand("list")
def listCommands(caller):
	commands=systemCS.functions.keys()
	commands.sort()
	return ' '.join(commands)

@CSCommand("say","trusted")
def say(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("say",[string])
	sbserver.message(string)
	return string

@CSCommand("echo")
def echo(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("echo",[caller,string])
	if caller[0]=="ingame":
		sbserver.playerMessage(caller[1],string)

@eventHandler('user_communication')
def usercommunicationingame(caller,msg):
	if caller[0]=="ingame":
		return
	sbserver.message(""+formatOwner(caller)+": "+msg)