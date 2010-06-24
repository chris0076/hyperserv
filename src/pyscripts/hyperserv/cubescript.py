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
	def executeby(self,owner,string):
		self.owner=owner
		print "setting owner to",self.owner
		return self.executestring(string)
		
def whoami(interpreter):
	print interpreter.owner

playerCS=CSInterpreterOwner()
playerCS.addfunction("outputfunction",lambda interpreter,msg: sbserver.message(msg))
playerCS.addfunction("map",lambda interpreter,name,mode=1: sbserver.setMap(name,mode))
playerCS.addfunction("whoami",whoami)

systemCS=CSInterpreterOwner(playerCS.functions.copy(),playerCS.variables)
systemCS.owner=("system","")


playerCS.executeby(("ingame",0),"echo (whoami)")
systemCS.executestring("echo (whoami)")
