import sbserver, sbevents
from ConfigParser import ConfigParser

limit = 5
duration = 3600

def onTeamkill(cn, tcn):
	if sbserver.playerTeamkills(cn) >= limit:
		sbevents.triggerEvent('player_ban', (cn, duration, 'Teamkilling'))

config = ConfigParser()
config.read('NoTeaKillers/plugin.conf')
if config.has_option('Config', 'limit'):
	limit = config.get('Config', 'limit')
if config.has_option('Config', 'duration'):
	duration = config.get('Config', 'duration')

sbevents.registerEventHandler('player_teamkill', onTeamkill)

