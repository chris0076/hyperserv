from hyperserv.events import eventHandler, triggerServerEvent
import sbserver
from lib.cubescript import CSInterpreter, CSError
from hyperserv.permissions import checkPermissions, PermissionError

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
		except PermissionError,e:
			print "%s was not allowed to execute %s" % (owner,string) #TODO: log this properly
			raise
		finally:
			self.owner=("nobody","")

systemCS=CSInterpreterOwner()
systemCS.owner=("system","")

playerCS=CSInterpreterOwner(systemCS.functions,systemCS.variables)
playerCS.owner=("nobody","") #have this for security, functions from playerCS should never be called as nobody

class CSCommand(object):
	def wrapper(self,f,*args):
		owner=args[0].owner
		checkPermissions(owner,self.permissionRequirement)
		return f(owner,*args[1:])
	
	def __init__(self, name, permissionRequirement="none"):
		self.name=name
		self.permissionRequirement=permissionRequirement
	
	def __call__(self,f):
		newfunction=lambda *args: self.wrapper(f,*args)
		systemCS.addfunction(self.name,newfunction)
		return newfunction

def checkforCS(caller,string):
	if string[0] in ['#','@']:
		try:
			playerCS.executeby(caller,string[1:])
		except Exception,e:
			playerCS.executeby(caller,"echo Error: \"%s\"" % (' '.join(e).replace('"','^"'),))
		return 1
	else:
		return 0