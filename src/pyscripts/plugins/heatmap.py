#!/usr/bin/env python
from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError
from hyperserv.position import getPosition
from editing.base import sendpacket
from editing.ents import ent

flamecolours = {
	"good": 0,
	"evil": 15,
	"neutral": 240,
}

@CSCommand("mark","trusted")
def mark(caller,color):
	cn=int(caller[1])
	color=flamecolours[color]
	position=map(lambda a: a*16, getPosition(cn))
	entity=(position[0],position[1],position[2]+64,5,0,0,0,color,0)
	ent(entity)
