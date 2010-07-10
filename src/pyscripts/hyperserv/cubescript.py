import sys,traceback

import sbserver
from hyperserv.events import eventHandler, triggerServerEvent
from lib.cubescript import CSParser, CSInterpreter, CSError
from hyperserv.permissions import UserSessionManager, PermissionError

class CSInterpreterOwner(CSInterpreter):
	def executeby(self,owner,string):
		while(self.owner[0]!="nobody"):
			pass #TODO: add logging here
		self.owner=owner
		try:
			return self.executestring(string)
		finally:
			self.owner=("nobody","")

systemCS=CSInterpreterOwner()
systemCS.owner=("system","")

playerCS=CSInterpreterOwner(systemCS.external,systemCS.variables)
playerCS.owner=("nobody","") #have this for security, functions from playerCS should never be called as nobody

class CSCommand(object):
	def wrapper(self,f,*args):
		owner=args[0].owner
		UserSessionManager.checkPermissions(owner,self.permissionRequirement)
		return f(owner,*args[1:])
	
	def __init__(self, name, permissionRequirement="none"):
		self.name=name
		self.permissionRequirement=permissionRequirement
	
	def __call__(self,f):
		functionpointer=lambda *args: self.wrapper(f,*args)
		systemCS.external[self.name]=functionpointer
		return f

def checkUntrustedCode(code):
	if type(code) is not list:
		return
	if code[0] in ["while","loop","alias","lambda"]:
		raise PermissionError("You're not allowed to use such complex code.")
	if len(code)>1 and code[1]=="=":
		raise PermissionError("You're not allowed to use such complex code.")
	for arg in code[1:]:
		checkUntrustedCode(arg)

def checkforCS(caller,string):
	if string[0] in ['#','@']:
		string=string[1:]
		try:
			try:
				UserSessionManager.checkPermissions(caller,"trusted")
			except PermissionError:
				checkUntrustedCode(CSParser(string).parse())
			playerCS.executeby(caller,string)
		except:
			exctype,exctext,exctraceback=sys.exc_info()
			errormsg="%s: %s" % (exctype.__name__, exctext)
			playerCS.executeby(caller,"echo \"%s\"" % (errormsg.replace('"','^"'),))
			raise
		return 1
	else:
		return 0

@CSCommand("say","trusted")
def say(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("say",[string])
	return string

@CSCommand("echo")
def echo(caller,*what):
	string=' '.join(map(str,what))
	triggerServerEvent("echo",[caller,string])
	return string