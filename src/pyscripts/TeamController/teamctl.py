from xsbs.events import registerServerEventHandler
from UserPrivilege.userpriv import masterRequired
from xsbs.ui import error
import sbserver

switchteam_modes = [
	4,
	6,
	8,
	11,
	12]

setteam_modes = [
	2,
	4]

def onSwitchTeam(cn, team):
	mode =  sbserver.gameMode()
	print 'switch team %i %s (%i)' % (cn, team, mode)
	if mode in setteam_modes:
		sbserver.setTeam(cn, team)
	elif mode in switchteam_modes:
		if team == 'good' or team == 'evil':
			sbserver.setTeam(cn, team)
		else:
			sbserver.playerMessage(cn, error('You cannot join specified team in current game mode.'))
	else:
		sbserver.playerMessage(cn, error('You can not set team in this game mode.'))

@masterRequired
def onSetTeam(cn, who, team):
	print 'set team'
	mode =  sbserver.gameMode()
	if mode not in setteam_modes:
		sbserver.playerMessage(cn, error('You can not set team in this game mode.'))
	else:
		sbserver.setTeam(who, team)

registerServerEventHandler('player_switch_team', onSwitchTeam)
registerServerEventHandler('player_set_team', onSetTeam)

