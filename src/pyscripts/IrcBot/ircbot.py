import sbevents, sbserver
import socket
from ConfigParser import ConfigParser

channel = ''
server = ''
nickname = ''
port = 6667

class IrcBot:
	def __init__(self, servername, nickname, port=6667):
		self.servername = servername
		self.nickname = nickname
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setblocking(0)
		self.isConnected = False
		self.channels = []
	def connect(self):
		sbevents.sockmon.onRead(self.socket, self.onConnect, (), False)
		try:
			self.socket.connect((self.servername, self.port))
		except:
			pass
	def onConnect(self):
		sbevents.sockmon.onRead(self.socket, self.processData, (), True)
		self.buff = self.socket.recv(4096)
		self.socket.send('NICK %s\r\n' % self.nickname)
		self.socket.send('USER %s %s %s :%s\r\n' % (self.nickname, self.nickname, self.nickname, self.nickname))
	def onWelcome(self):
		self.isConnected = True
		for channel in self.channels:
			self.join(channel)
		del self.channels[:]
	def join(self, channel):
		if self.isConnected:
			self.socket.send('JOIN %s\r\n' % channel)
		else:
			self.channels.append(channel)
	def privMsg(self, user, message):
		self.socket.send('PRIVMSG %s :%s\r\n' % (user, message))
	def processData(self):
		self.buff += self.socket.recv(4096)
		print self.buff,
		tmp_buff = self.buff.split('\n')
		self.buff = tmp_buff.pop()
		for line in tmp_buff:
			line = line.strip().split()
			if line[0] == 'PING':
				self.socket.send('PONG %s\r\n' % line[1])
			if line[1] == 'MODE':
				if not self.isConnected and line[3] == ':+iw':
					self.onWelcome()

config = ConfigParser()
config.read('IrcBot/plugin.conf')

if config.has_option('Bot', 'servername'):
	server = config.get('Bot', 'servername')
if config.has_option('Bot', 'channel'):
	channel = config.get('Bot', 'channel')
if config.has_option('Bot', 'nickname'):
	nickname = config.get('Bot', 'nickname')

if channel != '' and servername != '' and nickname != '':
	bot = IrcBot(server, nickname, port)
	bot.connect()
	bot.join(channel)
else:
	print 'Could not start IRC Bot.  You must supply a servername, channel, and nickname.'

def onPlayerActive(cn):
	bot.privMsg(channel, 'Player %s (%i) has joined' % (sbserver.playerName(cn), cn))

def onMsg(cn, text):
	bot.privMsg(channel, '%s (%i): %s' % (sbserver.playerName(cn), cn, text))

def onTeamMsg(cn, text):
	bot.privMsg(channel, '%s (%i) (Team): %s' % (sbserver.playerName(cn), cn, text))

if config.has_option('Abilities', 'player_active') and config.get('Abilities', 'player_active') == 'yes':
	sbevents.registerEventHandler('player_active', onPlayerActive)
if config.has_option('Abilities', 'message') and config.get('Abilities', 'message') == 'yes':
	sbevents.registerEventHandler('player_message', onMsg)
if config.has_option('Abilities', 'team_message') and config.get('Abilities', 'team_message') == 'yes':
	sbevents.registerEventHandler('player_message_team', onTeamMsg)
