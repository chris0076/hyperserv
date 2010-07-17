"""This file contains all the even handlers for notices"""
from hyperserv.events import eventHandler, triggerServerEvent

import hypershade
from hypershade.cubescript import CSCommand
from hypershade.util import modeName, mastermodeName, formatCaller

def serverNotice(string):
	triggerServerEvent("notice",[string])

@CSCommand("notice","admin")
def CSserverNotice(caller, *strings):
	string=' '.join(strings)
	if caller[0]=="system":
		serverNotice(string)
	else:
		serverNotice("Notice from %s: %s" % (formatCaller(caller),string))
	return string

@eventHandler('player_connect')
def noticePlayerConnect(cn):
	serverNotice("Connected: "+formatCaller(("ingame",cn))+"("+str(cn)+")")

@eventHandler('player_disconnect')
def noticePlayerDisconnect(cn):
	serverNotice("Disconnected: "+formatCaller(("ingame",cn))+"("+str(cn)+")")

@eventHandler('map_changed')
def noticeMapChanged(name,mode):
	serverNotice("Map: "+name+" ("+modeName(mode)+")")

@eventHandler('intermission_begin')
def noticeIntermissionBegin():
	serverNotice("Intermission.")

@eventHandler('server_mastermode_changed')
def noticeMastermodeChanged(number):
	serverNotice("Mastermode is now %s (%d)."  % (mastermodeName(number),number))

#master and admin stuff
@eventHandler("player_claimed_master")
def noticeClaimMaster(cn):
	serverNotice("%s claimed main master." % (formatCaller(("ingame",cn)),))

@eventHandler("player_claimed_admin")
def noticeClaimAdmin(cn):
	serverNotice("%s claimed main admin." % (formatCaller(("ingame",cn)),))

@eventHandler("player_released_master")
def noticeRelinquishMaster(cn):
	serverNotice("%s relinquished master." % (formatCaller(("ingame",cn)),))

@eventHandler("player_released_admin")
def noticeRelinquishAdmin(cn):
	serverNotice("%s relinquished admin." % (formatCaller(("ingame",cn)),))