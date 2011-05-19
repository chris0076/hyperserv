"""This file contains the required functions for the editing features"""

import sbserver
from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

def merge(a):
	return (reduce(lambda y,x: x*256+y, a, 0),)

def getposition(cn):
	a=sbserver.playerPosition(cn)
	#return a[0:4]+merge(a[4:7])+merge(a[7:10])+merge(a[10:13])+a[13:]
	return a

@CSCommand("pos","admin")
def getpositionCS(caller, cn=None):
	if cn is None:
		if caller[0]!="ingame":
			raise ServerError("You are not ingame. Please specify cn.")
		cn=int(caller[1])
	return ''.join(map(lambda x: str(x).rjust(5),getposition(int(cn))))

