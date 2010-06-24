#!/usr/bin/env python

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task, defer
from twisted.python import log

config = {
	"server": "irc.freenode.net",
	
	"channels": [
		"#hyperserv"
	],
	"nickname": "hyperserv_test",
	"short": "hs",
}



#**************
#
#  IRC Connection
#
#**************

class IRCBot(irc.IRCClient):
	nickname = config["nickname"]
	
	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		self.joined_channels = []

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)

	# callbacks for events

	def signedOn(self):
		"""Called when bot has succesfully signed on to server."""
		self.join(config["channels"][0])
		self.msg(config["channels"][0],"here I am!"+config["nickname"]+self.nickname+"!")
		
		for channel in config["channels"][1:]:
			self.join(channel)
		
		print "Signed on IRC"

	def joined(self, channel):
		if channel not in self.joined_channels:
			self.joined_channels.append(channel)

	def userJoined(self, user, channel):
		pass
	
	def left(self, channel):
		if channel in self.joined_channels:
			self.joined_channels.remove(channel)

	def broadcast(self, msg):
		for channel in self.joined_channels:
			self.say(channel, msg)

	def privmsg(self, user, channel, msg):
		"""This will get called when the bot receives a message."""
		user = user.split('!', 1)[0]
		
		if user=="Q":
			return
		
		# Check to see if they're sending me a private message
		if channel == self.nickname:
			self.say(user, "i'm just a bot");
			return
		
		# Directed at me?
		if msg.startswith(self.nickname + ":"):
			self.say(channel, "long");
			
		if msg.startswith(config["short"]):
			self.say(channel, "long");

	def action(self, user, channel, msg):
		"""This will get called when the bot sees someone do an action."""
		#user = user.split('!', 1)[0]
		#self.logger.log("* %s %s" % (user, msg))\
		pass

	# irc callbacks

	def irc_NICK(self, prefix, params):
		"""Called when an IRC user changes their nickname."""
		old_nick = prefix.split('!')[0]
		new_nick = params[0]
		pass


	# For fun, override the method that determines how a nickname is changed on
	# collisions. The default method appends an underscore.
	def alterCollidedNick(self, nickname):
		"""
		Generate an altered version of a nickname that caused a collision in an
		effort to create an unused related name for subsequent registration.
		"""
		return nickname + '_'

class IRCBotFactory(protocol.ClientFactory):
	"""A factory for IRCBots.

	A new protocol instance will be created each time we connect to the server.
	"""

	# the class of the protocol to build when new connection is made
	protocol = IRCBot

	def __init__(self):
		pass

	def clientConnectionLost(self, connector, reason):
		"""If we get disconnected, reconnect to server."""
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "connection failed:", reason
		reactor.stop()

if __name__ == '__main__':
	# create factory protocol and application
	f = IRCBotFactory()

	# connect factory to this host and port
	reactor.connectTCP(config["server"], 6667, f)
	
	# run bot
	reactor.run()