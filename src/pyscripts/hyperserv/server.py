"""This file contains all the basic commands that the server needs to be playable, this does not handle '/' type requests from clients only server-side cubescript commands"""
from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from hyperserv.cubescript import systemCS, CSCommand
from hyperserv.util import ipLongToString, modeNumber, mastermodeNumber

class ServerError(Exception): pass

@CSCommand("map","master")
def changeMap(caller,name,mode=None):
	if mode is None:
		mode=sbserver.gameMode()
	return sbserver.setMap(name,modeNumber(mode))

@CSCommand("master","master")
def setMaster(caller):
	if(caller[0]=="ingame"):
		return sbserver.setMaster(caller[1])
	raise ServerError("You are not ingame.")
	return

@CSCommand("admin","admin")
def setAdmin(caller):
	if(caller[0]=="ingame"):
		return sbserver.setAdmin(caller[1])
	raise ServerError("You are not ingame.")
	return

@CSCommand("relinquish")
def setAdmin(caller):
	if(caller[0]=="ingame"):
		return sbserver.resetPrivilege(caller[1])
	raise ServerError("You are not ingame.")
	return

@CSCommand("mastermode","master")
def masterMode(caller,name=None):
	if name==None:
		return sbserver.masterMode()
	return sbserver.setMasterMode(mastermodeNumber(name))

@CSCommand("who")
def who(caller,where="ingame"):
	if where=="ingame":
		def cndetails(cn):
			return sbserver.playerName(cn)+" (cn"+str(cn)+"/"+ipLongToString(sbserver.playerIpLong(cn))+")"
		return '; '.join(map(cndetails,sbserver.clients()))

@CSCommand("list")
def listCommands(caller,which="hyperserv"):
	"""List all commands available"""
	if which=="all":
		commands=systemCS.functions.keys()+systemCS.external.keys()
	elif which=="cubescript":
		commands=systemCS.functions.keys()
	else:
		commands=systemCS.external.keys()
	commands.sort()
	return ' '.join(commands)

@CSCommand("say","trusted")
def say(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("say",[string])
	return string

@CSCommand("echo")
def echo(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("echo",[caller,string])
	return string
