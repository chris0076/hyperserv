from hyperserv.events import eventHandler
import sbserver
from lib.cubescript import CSInterpreter, CSError

@eventHandler('player_message')
def PlayerMessage(a,b):
	if(b.startswith("#")):
		try:
			playerCS.executeby(("ingame",a),b[1:])
		except CSError,e:
			playerCS.executeby(("ingame",a),"echo Error: "+' '.join(e))

class CSInterpreterOwner(CSInterpreter):
	def executeby(self,owner,string): #TODO: add logging here
		while(self.owner[0]!="nobody"):
			pass
		self.owner=owner
		try:
			returns=self.executestring(string)
		finally:
			self.owner=("nobody","")

systemCS=CSInterpreterOwner()
systemCS.owner=("system","")
systemCS.addfunction("outputfunction",lambda interpreter,msg: sbserver.message(msg))

playerCS=CSInterpreterOwner(systemCS.functions,systemCS.variables)
playerCS.owner=("nobody","") #have this for security, functions from playerCS should never be called as nobody