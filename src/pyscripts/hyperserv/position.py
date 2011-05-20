"""This file contains the required functions for the editing features"""

import sbserver
from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

def merge(a):
	return (reduce(lambda y,x: x*256+y, a, 0),)

def getPosition(cn):
	return sbserver.playerPosition(cn)[:3]
	
def getYaw(cn):
	return sbserver.playerPosition(cn)[3]

@CSCommand("pos","master")
def getPositionCS(caller, cn=None):
	if cn is None:
		if caller[0]!="ingame":
			raise ServerError("You are not ingame. Please specify cn.")
		cn=int(caller[1])
	return "Pos: %s, Yaw: %s" %(getPosition(int(cn)),getYaw(int(cn)))

