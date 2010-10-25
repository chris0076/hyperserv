#!/usr/bin/env python


# Urwid
import urwid
import urwid.curses_display

#twisted
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

#hyperserv
from hyperserv.events import eventHandler, triggerServerEvent
from hypershade.config import config
from hypershade.cubescript import checkforCS
from hypershade.usersession import UserSessionManager
from hypershade.util import formatCaller

class CursesStdIO:
    """fake fd to be registered as a reader with the twisted reactor.
       Curses classes needing input should extend this"""

    def fileno(self):
        """ We want to select on FD 0 """
        return 0

    def doRead(self):
        """called when input is ready"""

    def logPrefix(self): return 'CursesClient'

class Screen(CursesStdIO):
	def __init__(self, tui):
		self.tui = tui

	def init(self):
		self.size = self.tui.get_cols_rows()

		self.lines = [urwid.Text('HyperServ Console, User %s' % (user,))]
		self.listbox = urwid.ListBox(self.lines)
		self.input = urwid.Edit()

		self.frame = urwid.Frame(self.listbox, footer = self.input)
		self.frame.set_focus('footer')

		self.redisplay()

	def addLine(self, text):
		""" add a line to the internal list of lines"""

		self.lines.append(urwid.Text(text))
		self.listbox.set_focus(len(self.lines) - 1)
		self.redisplay()

	def redisplay(self):
		""" method for redisplaying lines 
			based on internal list of lines """

		canvas = self.frame.render(self.size, focus = True)
		self.tui.draw_screen(self.size, canvas)

	def doRead(self):
		""" Input is ready! """
		keys = self.tui.get_input()

		for key in keys:
			if key == 'window resize':
				self.size = self.tui.get_cols_rows()
			elif key == 'enter':
				text = self.input.get_edit_text()
				self.input.set_edit_text('')
				if(checkforCS(user,text)==0):
					triggerServerEvent("user_communication",[("console",config["consoleuser"]),text])
			elif key in ('up', 'down', 'page up', 'page down'):
				self.listbox.keypress(self.size, key)
			else:
				self.frame.keypress(self.size, key)

		self.redisplay()

	def connectionLost(self, failure):
		pass

user=("console",config["consoleuser"])
UserSessionManager[user]=(config["consoleuser"],"admin")

@eventHandler('echo')
def echoconsole(caller,msg):
	if caller==user:
		screen.addLine(msg)

@eventHandler('say')
def sayconsole(msg):
	screen.addLine(msg)

@eventHandler('user_communication')
def usercommunicationconsole(caller,msg):
	screen.addLine(formatCaller(caller)+": "+msg)
	
@eventHandler('notice')
def noticeconsole(msg):
	screen.addLine("Notice: "+msg)

tui = urwid.curses_display.Screen()
screen = Screen(tui)

tui.start()
reactor.callWhenRunning(screen.init)
reactor.addReader(screen)