"""This file contains all the even handlers for notices"""
from hyperserv.events import eventHandler, triggerServerEvent

import hypershade
from hypershade.cubescript import CSCommand, playerCS
from hypershade.util import modeName, mastermodeName, formatCaller

def serverNotice(string):
	print "Notice: ",string
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

@eventHandler("player_spectated")
def noticePlayerSpectated(cn):
	serverNotice("%s is now a spectator." % (formatCaller(("ingame",cn)),))

@eventHandler("player_unspectated")
def noticePlayerUnSpectated(cn):
	serverNotice("%s is no longer a spectator." % (formatCaller(("ingame",cn)),))

@eventHandler("player_editmuted")
def noticePlayerEditMuted(cn):
	serverNotice("%s is now edit muted." % (formatCaller(("ingame",cn)),))

@eventHandler("player_editunmuted")
def noticePlayerEditUnMuted(cn):
	serverNotice("%s is no longer edit muted." % (formatCaller(("ingame",cn)),))

@eventHandler("player_kicked")
def noticePlayerUnSpectated(caller,cn):
	serverNotice("%s got kicked by %s." % (formatCaller(("ingame",cn)),formatCaller(caller)))

@eventHandler("player_uploaded_map")
def noticePlayerUploadedMap(cn):
	serverNotice("%s has sent the map." % (formatCaller(("ingame",cn)),))

@eventHandler("player_get_map")
def noticePlayerGetMap(cn):
	serverNotice("%s is getting the map." % (formatCaller(("ingame",cn)),))

@eventHandler("player_name_changed")
def noticeNameChange(cn,namefrom,nameto):
	serverNotice("%s changed his name to %s." % (namefrom,nameto))

@eventHandler('player_auth_succeed')
def noticeAuth(cn,name):
	serverNotice("%s authed as '%s'." % (formatCaller(("ingame",cn)),name))

@eventHandler('edit_blocked')
def noticeEditMute(cn):
	caller=("ingame",cn)
	playerCS.executeby(caller,"echo \"%s is edit muted.\"" % (formatCaller(caller)))