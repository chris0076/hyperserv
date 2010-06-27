from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from lib.cubescript import CSInterpreter, CSError

@eventHandler('player_message')
def PlayerMessage(cn,msg):
	if checkforCS(("ingame",cn),msg)==0:
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

class CSCommand(object):
	def __init__(self, name):
		self.name=name
	def __call__(self,f):
		newfunction=lambda interpreter, *args: f(interpreter.owner,*args)
		systemCS.addfunction(self.name,newfunction)
		return newfunction

def checkforCS(caller,string):
	if string[0] in ['#','@']:
		try:
			playerCS.executeby(caller,string[1:])
		except Exception,e:
			print caller
			playerCS.executeby(caller,"echo Error: "+' '.join(e))
		return 1
	else:
		return 0