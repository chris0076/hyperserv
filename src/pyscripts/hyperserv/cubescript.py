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
	def executeby(self,owner,string): #TODO: add logging here
		while(self.owner[0]!="nobody"):
			pass
		self.owner=owner
		try:
			returns=self.executestring(string)
		finally:
			self.owner=("nobody","")
		
def whoami(interpreter):
	return str(interpreter.owner)

def echo(interpreter,msg):
	print msg

systemCS=CSInterpreterOwner()
systemCS.owner=("system","")
#systemCS.addfunction("outputfunction",lambda interpreter,msg: sbserver.message(msg))
systemCS.addfunction("outputfunction",echo)
systemCS.addfunction("map",lambda interpreter,name,mode=1: sbserver.setMap(name,mode))
systemCS.addfunction("whoami",whoami)

playerCS=CSInterpreterOwner(systemCS.functions,systemCS.variables)
playerCS.owner=("nobody","") #have this for security, functions from playerCS should never be called as nobody

##demo for this commit
systemCS.executestring("echo systemCS.executestring (whoami)")
playerCS.executestring("echo playerCS.executestring (whoami)")
playerCS.executeby(("ingame",0),"echo playerCS.executeby (whoami)")
playerCS.executestring("echo playerCS.executestring again (whoami)")