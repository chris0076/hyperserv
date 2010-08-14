"""This file contains all the basic commands that the server needs to be playable, this does not handle '/' type requests from clients only server-side cubescript commands"""

import sbserver
from datetime import timedelta, datetime

from hyperserv.events import eventHandler, triggerServerEvent

from hypershade.config import config
from hypershade.cubescript import systemCS, CSCommand
from hypershade.usersession import UserSessionManager
from hypershade.util import ipLongToString, modeNumber, mastermodeNumber, formatCaller

from hypershade.bandatabase import bandatabase

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

@CSCommand("kick","master")
def kick(caller,cn):
	cn=int(cn)
	UserSessionManager.checkPermissions(caller,UserSessionManager[("ingame",cn)][1]) #check if the other person is more privileged
	
	ban(caller,sbserver.playerName(cn),"kicked by %s" % formatCaller(caller))
	triggerServerEvent("player_kicked",[caller,cn])
	return sbserver.playerKick(cn)

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
		if boolean==0 and sbserver.masterMode()>=2:
			UserSessionManager.checkPermissions(caller,"master")
		spectatorHelpler(boolean,cn)
	else:
		UserSessionManager.checkPermissions(caller,"master")
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
	mastermode=mastermodeNumber(name)
	
	if config["serverpublic"]=="1":
		if mastermode>=2:
			UserSessionManager.checkPermissions(caller,"trusted")
	if config["serverpublic"]=="2":
		if mastermode>=3:
			UserSessionManager.checkPermissions(caller,"trusted")
	
	return sbserver.setMasterMode(mastermode)

@CSCommand("who")
def who(caller,where="ingame"):
	if where=="ingame":
		def cndetails(cn):
			return sbserver.playerName(cn)+" (cn"+str(cn)+"/"+ipLongToString(sbserver.playerIpLong(cn))+")"
		
		string='; '.join(map(cndetails,sbserver.clients()))
		if string is not "":
			return string
		else:
			return "No players on this server."

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

@CSCommand("ban","trusted")
def ban(caller,who=None,reason="",time="60"):
	if who is None:
		bans(caller)
	
	try:
		who=sbserver.playerName(int(who))
	except ValueError:
		pass
	
	if time[-1]=="d":
		time=int(time[:1])*1440
	
	if time in ["perm","permanent","permanently","0",0]:
		expires=None
	else:
		expires=datetime.utcnow()+timedelta(0,int(time)*60)
	
	bandatabase[who]=(expires,reason)

@CSCommand("bans","master")
def bans(caller):
	return bandatabase

@CSCommand("delban","trusted")
def delban(caller,who):
	del bandatabase[who]

@CSCommand("minsleft")
def minsleft(caller,time=None):
	if time is not None:
		UserSessionManager.checkPermissions(caller,"trusted")
		sbserver.setMinsRemaining(int(time))
	return sbserver.minutesRemaining()/60 #todo, fix the api, it shouldn't return seconds...