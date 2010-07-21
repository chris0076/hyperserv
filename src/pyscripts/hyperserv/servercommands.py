"""This file contains all the basic commands that the server needs to be playable, this does not handle '/' type requests from clients only server-side cubescript commands"""

import sbserver
from hyperserv.events import eventHandler, triggerServerEvent

from hypershade.cubescript import systemCS, CSCommand
from hypershade.usersession import UserSessionManager
from hypershade.util import ipLongToString, modeNumber, mastermodeNumber

class ServerError(Exception): pass

@CSCommand("map","master")
def changeMap(caller,name,mode=None):
	if mode is None:
		mode=sbserver.gameMode()
	return sbserver.setMap(name,modeNumber(mode))
systemCS.executestring("map mediterranean insta") #first map

@CSCommand("master","master")
def setMaster(caller):
	if(caller[0]=="ingame"):
		return sbserver.setMaster(caller[1])
	raise ServerError("You are not ingame.")
	return

@CSCommand("admin","admin")
def setAdmin(caller):
	if(caller[0]=="ingame"):
		print caller[1]
		return sbserver.setAdmin(caller[1])
	raise ServerError("You are not ingame.")
	return

@CSCommand("relinquish")
def setAdmin(caller):
	if(caller[0]=="ingame"):
		return sbserver.resetPrivilege(caller[1])
	raise ServerError("You are not ingame.")
	return

@CSCommand("kick","master")
def kick(caller,cn):
	return sbserver.playerKick(int(cn))

@CSCommand("spectator")
def spectator(caller,boolean=None,cn=None):
	#empty args
	if boolean is None:
		boolean=1
	boolean=int(boolean)
	
	if cn is None:
		if(caller[0]=="ingame"):
			cn=caller[1]
		else:
			raise ServerError("You are not ingame. Please specify cn.")
	cn=int(cn)
	
	#check if it's a self call
	if caller[1]==cn:
		spectatorHelpler(boolean,cn)
	else:
		UserSessionManager.checkPermissions(UserSessionManager[caller[1]],"master")
		spectatorHelpler(boolean,cn)

def spectatorHelpler(boolean,cn):
	if boolean:
		sbserver.spectate(cn)
	else:
		sbserver.unspectate(cn)

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
