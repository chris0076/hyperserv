"""This file contains all the basic commands that the server needs to be playable, this does not handle '/' type requests from clients only server-side cubescript commands"""
from hyperserv.events import eventHandler
import sbserver
from hyperserv.cubescript import systemCS
from hyperserv.permissions import masterRequired, adminRequired
from hyperserv.net import ipLongToString

def whoami(caller):
	return str(caller)
systemCS.addfunction("whoami",whoami)

@masterRequired
def changeMap(caller,name,mode=1):
	return sbserver.setMap(name,mode)
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