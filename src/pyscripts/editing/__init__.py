"""This file contains the required functions for the editing features"""

import sbserver
from hypershade.cubescript import playerCS, CSCommand
from hypershade.config import config
from hyperserv.events import eventHandler, triggerServerEvent
from hyperserv.servercommands import ServerError
from hyperserv.notices import serverNotice
from hypershade.util import formatCaller

packettypes = [
('CONNECT', 0), ('SERVINFO', 0), ('WELCOME', 2), ('INITCLIENT', 0), ('POS', 0), ('TEXT', 0), 
('SOUND', 2), ('CDIS', 2), ('SHOOT', 0), ('EXPLODE', 0), ('SUICIDE', 1), ('DIED', 4),
('DAMAGE', 6), ('HITPUSH', 7), ('SHOTFX', 10), ('EXPLODEFX', 4), ('TRYSPAWN', 1), ('SPAWNSTATE', 14),
('SPAWN', 3), ('FORCEDEATH', 2), ('GUNSELECT', 2), ('TAUNT', 1), ('MAPCHANGE', 0), ('MAPVOTE', 0),
('ITEMSPAWN', 2), ('ITEMPICKUP', 2), ('ITEMACC', 3), ('TELEPORT', -1), ('JUMPPAD', -1), ('PING', 2),
('PONG', 2), ('CLIENTPING', 2), ('TIMEUP', 2), ('MAPRELOAD', 1), ('FORCEINTERMISSION', 1), ('SERVMSG', 0),
('ITEMLIST', 0), ('RESUME', 0), ('EDITMODE', 2), ('EDITENT', 11), ('EDITF', 16), ('EDITT', 16),
('EDITM', 16), ('FLIP', 14), ('COPY', 14), ('PASTE', 14), ('ROTATE', 15), ('REPLACE', 17),
('DELCUBE', 14), ('REMIP', 1), ('NEWMAP', 2), ('GETMAP', 1), ('SENDMAP', 0), ('CLIPBOARD', -1),
('EDITVAR', 0), ('MASTERMODE', 2), ('KICK', 2), ('CLEARBANS', 1), ('CURRENTMASTER', 4), ('SPECTATOR', 3),
('SETMASTER', 0), ('SETTEAM', 0), ('BASES', 0), ('BASEINFO', 0), ('BASESCORE', 0), ('REPAMMO', 1),
('BASEREGEN', 6), ('ANNOUNCE', 2), ('LISTDEMOS', 1), ('SENDDEMOLIST', 0), ('GETDEMO', 2), ('SENDDEMO', 0),
('DEMOPLAYBACK', 3), ('RECORDDEMO', 2), ('STOPDEMO', 1), ('CLEARDEMOS', 2), ('TAKEFLAG', 3), ('RETURNFLAG', 4),
('RESETFLAG', 6), ('INVISFLAG', 3), ('TRYDROPFLAG', 1), ('DROPFLAG', 7), ('SCOREFLAG', 10), ('INITFLAGS', 0),
('SAYTEAM', 0), ('CLIENT', 0), ('AUTHTRY', 0), ('AUTHCHAL', 0), ('AUTHANS', 0), ('REQAUTH', 0),
('PAUSEGAME', 2), ('ADDBOT', 2), ('DELBOT', 1), ('INITAI', 0), ('FROMAI', 2), ('BOTLIMIT', 2),
('BOTBALANCE', 2), ('MAPCRC', 0), ('CHECKMAPS', 1), ('SWITCHNAME', 0), ('SWITCHMODEL', 2), ('SWITCHTEAM', 0),
('INITAI', -1), ('FROMAI', -1), ('BOTLIMIT', -1), ('BOTBALANCE', -1), ('MAPCRC', -1), ('CHECKMAPS', -1),
('SWITCHNAME', -1), ('SWITCHMODEL', -1), ('SWITCHTEAM', -1)]

def packettypename(number):
	return packettypes[int(number)][0]

def packettypenumber(name):
	for number,packettype in enumerate(packettypes):
		if packettype[0]==name:
			return number
	return int(name)
 
@CSCommand("sendpacket","admin")
def sendpacketcommand(caller,*args):
	sendpacket(*args)

def sendpacket(*args):
	if len(args)==0:
		return
	packettype=packettypes[packettypenumber(args[0])]
	if (packettype[1]!=-1 and len(args)!=packettype[1]):
		raise ServerError("%s must have %s arguments." % packettype)
	mapdata=sbserver.sendPacket(*map(packettypenumber,args))

@eventHandler("edit_packet")
def noticeEditPacket(cn,packettype,*data):
	if config["editpacketnotices"]=="yes":
		serverNotice("Edit Packet from %s: %s %s" % (formatCaller(("ingame",cn)),packettypes[packettype][0],' '.join(map(str,data))))