from hyperserv.events import eventHandler
import sbserver
from lib.cubescript import CSInterpreter, CSError

@eventHandler('player_message')
def PlayerMessage(a,b):
	if(b.startswith("#")):
		try:
			interpreter.executestring(b[1:])
		except CSError,e:
			interpreter.executestring("echo Error: "+' '.join(e))

interpreter=CSInterpreter()
interpreter.functions["outputfunction"]=sbserver.message