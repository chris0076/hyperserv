from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from lib.cubescript import CSInterpreter, CSError

@eventHandler('player_message')
def PlayerMessage(cn,msg):
	if(msg.startswith("#")):
		try:
			playerCS.executeby(("ingame",cn),msg[1:])
		except CSError,e:
			playerCS.executeby(("ingame",cn),"echo Error: "+' '.join(e))
	else:
		triggerServerEvent("user_communication",[("ingame",cn),msg])
	

class CSInterpreterOwner(CSInterpreter):
	def executeby(self,owner,string):
		while(self.owner[0]!="nobody"):
			pass #TODO: add logging here
		self.owner=owner
		try:
			returns=self.executestring(string)
		finally:
			self.owner=("nobody","")

systemCS=CSInterpreterOwner()
systemCS.owner=("system","")

playerCS=CSInterpreterOwner(systemCS.functions,systemCS.variables)
playerCS.owner=("nobody","") #have this for security, functions from playerCS should never be called as nobody