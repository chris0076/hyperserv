from hyperserv.events import eventHandler
import sbserver
from lib.cubescript import CSInterpreter, CSError

@eventHandler('player_message')
def PlayerMessage(a,b):
	if(b.startswith("#")):
		try:
			playerCS.executeby(a,b[1:])
		except CSError,e:
			playerCS.executeby(a,"echo Error: "+' '.join(e))

class CSInterpreterOwner(CSInterpreter):
	owner=""
	def executeby(self,owner,string):
		self.owner=owner
		print "setting owner to",owner
		return self.executestring(string)

systemCS=CSInterpreterOwner()
systemCS.addfunction("outputfunction",lambda interpreter,msg: sbserver.message(msg))
systemCS.addfunction("map",lambda interpreter,name,mode=1: sbserver.setMap(name,mode))
systemCS.addfunction("whoami",lambda interpreter: "cs"+str(interpreter.owner))
playerCS=CSInterpreterOwner(systemCS.functions,systemCS.variables)