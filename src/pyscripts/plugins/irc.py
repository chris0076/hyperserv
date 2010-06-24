#!/usr/bin/env python

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task, defer

import sbserver

from hyperserv.events import eventHandler, triggerServerEvent
from hyperserv.cubescript import playerCS, CSError
from hyperserv.util import formatOwner

config = {
	"server": "irc.freenode.net",
	
	"channels": [
		"#hyperserv"
	],
	
	"nickname": "hyperserv_test",
	"short": "hs",
}

class IrcBot(irc.IRCClient):
	def connectionMade(self):
		self.nickname = self.factory.nickname
		irc.IRCClient.connectionMade(self)
		self.joined_channels = []
	def signedOn(self):
		for channel in self.factory.channels:
			self.join(channel)
		self.factory.signedOn(self)
	def connectionLost(self, reason):
		self.factory.signedOut(self)
	def joined(self, channel):
		if channel not in self.joined_channels:
			self.joined_channels.append(channel)
	def left(self, channel):
		if channel in self.joined_channels:
			self.joined_channels.remove(channel)
	def broadcast(self, message):
		for channel in self.joined_channels:
			self.say(channel, message)
	def privmsg(self, user, channel, msg):
		if channel != self.nickname:
			user = user.split('!', 1)[0]
			if(msg.startswith("#")):
				try:
					playerCS.executeby(("irc",user),msg[1:])
				except CSError,e:
					playerCS.executeby(("irc",user),"echo Error: "+' '.join(e))
			else:
				triggerServerEvent("user_communication",[("irc",user),msg])
	def alterCollidedNick(self, nickname):
		return nickname + '_'

class IrcBotFactory(protocol.ClientFactory):
	protocol = IrcBot
	def __init__(self, nickname, channels):
		self.nickname = nickname
		self.channels = channels
		self.bots = []
		self.reconnect_count = 0
	def doConnect(self):
		reactor.connectTCP(config['server'], 6667, factory)
	def doReconnect(self):
		if self.reconnect_count < 5:
			self.reconnect_count += 1
			self.doConnect()
	def signedOn(self, bot):
		if bot not in self.bots:
			self.bots.append(bot)
	def signedOut(self, bot):
		if bot in self.bots:
			self.bots.remove(bot)
			addTimer(5000, self.doReconnect, ())
	def broadcast(self, message):
		for bot in self.bots:
			bot.broadcast(message)
	def notice(self, nick, message):
		for bot in self.bots:
			bot.notice(nick,message)

# create factory protocol and application
factory = IrcBotFactory(config['nickname'], config['channels'])
factory.doConnect()

@eventHandler('say')
def sayirc(msg):
	factory.broadcast(msg)

@eventHandler('user_communication')
def usercommunicationirc(who,msg):
	if who[0]=="irc":
		return
	factory.broadcast("<"+formatOwner(who)+"> "+msg)

@eventHandler('echo')
def ircecho(who,msg):
	if who[0]=="irc":
		factory.notice(who[1],msg)