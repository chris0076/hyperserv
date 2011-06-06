#!/usr/bin/env python
import sbserver
from hypershade.cubescript import playerCS, CSCommand, threaded
from hyperserv.servercommands import ServerError
from hyperserv.position import getPosition
from editing.ents import ent
from hypershade.config import config
from hypershade.files import openfile
from hyperserv.events import eventHandler

flamecolour = {
	"good": 0,
	"evil": 15,
	"neutral": 240,
}

@CSCommand("mark","trusted")
def mark(caller):
	cn=int(caller[1])
	position=map(lambda a: a*16, getPosition(cn))
	entity=(position[0],position[1],position[2]+64,5,0,0,0,flamecolour[sbserver.playerTeam(cn)],0)
	ent(entity)

@eventHandler("player_frag")
def player_frag(killer, victim):
	victimposition=map(lambda a: a*16, getPosition(victim))
	ent((victimposition[0],victimposition[1],victimposition[2]+64,1,32,0,64,127,0))
	attackerposition=map(lambda a: a*16, getPosition(killer))
	ent((attackerposition[0],attackerposition[1],attackerposition[2]+64,1,32,127,0,0,0))

@CSCommand("acdatafrag", "trusted")
@threaded
def acdatafrag(caller, filename="killdata.txt"):
        f = openfile(filename, "r")[1]
        lines = f.readlines() 
        for line in lines:
            a = line[:-2].split(' ')
            victimposition=map(lambda a: a*16, (int(a[4]), int(a[5]), int(a[6])))
            ent((victimposition[0],victimposition[1],victimposition[2]+32,1,32,0,64,127,0))
            attackerposition=map(lambda a: a*16, (int(a[7]), int(a[8]), int(a[9])))
            ent((attackerposition[0],attackerposition[1],attackerposition[2]+32,1,32,127,0,0,0))
