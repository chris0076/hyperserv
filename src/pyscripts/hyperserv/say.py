from hyperserv.events import eventHandler
import sbserver

@eventHandler('player_message')
def PlayerMessage(a,b):
	print a,b
	sbserver.message(str(a)+str(b))

print "say.py loaded"