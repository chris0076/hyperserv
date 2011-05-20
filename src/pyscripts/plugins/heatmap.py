#!/usr/bin/env python
from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError
from hyperserv.position import getPosition
from editing.base import sendpacket

count=0

@CSCommand("mark","master")
def mark(caller,color):
	global count
	color=int(color)
	color=[15,2840][color]
	cn=int(caller[1])
	position=map(lambda a: a*16, getPosition(cn))
	packet=("EDITENT",count,position[0],position[1],position[2]+128,5,0,0,0,color,0)
	count=count+1
	print packet
	sendpacket(("system",""),*packet)
	print "done"
