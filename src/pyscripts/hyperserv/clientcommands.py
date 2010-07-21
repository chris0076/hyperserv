""" handle '/' type requests from clients and translate them into cubescript"""

import sbserver
from hyperserv.events import eventHandler
from hyperserv.servercommands import ServerError

from hypershade.cubescript import checkforCS
from hypershade.usersession import UserSessionManager

@eventHandler("player_setmaster")
def clientSetMaster(caller,text):
	checkforCS(("ingame",caller),"@login %s" % text)

@eventHandler("player_setmaster_off")
def clientLoseMaster(caller):
	checkforCS(("ingame",caller),"@logout")

@eventHandler("player_request_spectate")
def clientSpectate(caller,who):
	checkforCS(("ingame",caller),"@spectator 1 %s" % who)

@eventHandler("player_request_unspectate")
def clientUnspectate(caller,who):
	checkforCS(("ingame",caller),"@spectator 0 %s" % who)

@eventHandler("player_map_vote")
def clientMapVote(caller,mapname,mode):
	checkforCS(("ingame",caller),"@map %s %s" % (mapname,mode))

@eventHandler("player_set_mastermode")
def clientMastermode(caller,mastermode):
	checkforCS(("ingame",caller),"@mastermode %s" % mastermode)

@eventHandler("player_kick")
def clientKick(caller,who):
	#TODO: fix this kick event mess, both the notice and this
	print "kick",caller,who