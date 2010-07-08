"""This file contains all the even handlers for notices"""
import sbserver
from hyperserv.events import eventHandler, triggerServerEvent
from hyperserv.util import modeName, mastermodeName

def serverNotice(string):
	triggerServerEvent("notice",[string])

@eventHandler('player_connect')
def noticePlayerConnect(cn):
	serverNotice("Connected: "+sbserver.playerName(cn)+"("+str(cn)+")")

@eventHandler('player_disconnect')
def noticePlayerDisconnect(cn):
	serverNotice("Disconnected: "+sbserver.playerName(cn)+"("+str(cn)+")")

@eventHandler('map_changed')
def noticeMapChanged(name,mode):
	serverNotice("Map: "+name+" ("+modeName(mode)+")")

@eventHandler('intermission_begin')
def noticeIntermissionBegin():
	serverNotice("Intermission.")

@eventHandler('server_mastermode_changed')
def noticeMastermodeChanged(number):
	serverNotice("Mastermode is now %s (%d)." %(mastermodeName(number),number))

#master and admin stuff
@eventHandler("player_claimed_master")
def noticeClaimMaster(cn):
	serverNotice("%s claimed main master." % (sbserver.playerName(cn),))

@eventHandler("player_claimed_admin")
def noticeClaimAdmin(cn):
	serverNotice("%s claimed main admin." % (sbserver.playerName(cn),))

@eventHandler("player_released_master")
def noticeRelinquishMaster(cn):
	serverNotice("%s relinquished master." % (sbserver.playerName(cn),))

@eventHandler("player_released_admin")
def noticeRelinquishAdmin(cn):
	serverNotice("%s relinquished admin." % (sbserver.playerName(cn),))