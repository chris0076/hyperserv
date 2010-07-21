""" handle '/' type requests from clients and translate them into cubescript"""

import sbserver
from hyperserv.events import eventHandler
from hyperserv.servercommands import ServerError

from hypershade.cubescript import playerCS, systemCS
from hypershade.usersession import UserSessionManager

@eventHandler("player_setmaster")
def clientSetMaster(caller,text):
	playerCS.executeby(("ingame",caller),"login %s" % text)

@eventHandler("player_setmaster_off")
def clientLoseMaster(caller):
	playerCS.executeby(("ingame",caller),"logout")

@eventHandler("player_request_spectate")
def clientSpectate(caller,who):
	playerCS.executeby(("ingame",caller),"spectator 1 %s" % who)

@eventHandler("player_request_unspectate")
def clientUnspectate(caller,who):
	playerCS.executeby(("ingame",caller),"spectator 0 %s" % who)

@eventHandler("player_map_vote")
def clientMapVote(caller,mapname,mode):
	playerCS.executeby(("ingame",caller),"map %s %s" % (mapname,mode))

@eventHandler("player_kick")
def clientKick(caller,who):
	#TODO: fix this kick event mess, both the notice and this
	print "kick",caller,who