from hypershade.cubescript import CSCommand, systemCS, playerCS, escape

from hypershade.usersession import UserSessionManager, PermissionError
from hypershade.userdatabase import userdatabase

from hypershade.util import formatCaller

@CSCommand("login")
def login(caller,*params):
	username=None
	password=None
	
	if UserSessionManager[caller][0]!="notloggedin":
		username=UserSessionManager[caller][0]
		logout(caller)
	
	#extract username and password
	if len(params)==2:
		username=params[0]
		password=params[1]
	elif len(params)==1:
		password=params[0]
	
	#guess username
	if username is None:
		if caller[0]=="irc":
			user=userdatabase.search("irc nick",formatCaller(caller))
		elif caller[0]=="ingame":
			user=userdatabase.search("sauerbraten name",formatCaller(caller))
		else:
			raise ValueError("Could not determine your login name.")
		if user is None:
			raise ValueError("Could not determine your login name. Use \"@login username password\" to specify.")
	else:
		user=userdatabase[username]
	
	#temporarly cache the user instance
	user=dict(user.items())
	
	#authenticate with everything's that's available
	if password is None:
		if caller[0]=="irc":
			#call an ident message, TODO
			pass
		if caller[0]=="ingame":
			#this can only be verified with auth, and that's user initiated
			pass
		else:
			#hostname based
			pass
	else:
		if user["password"]==password:
			succeed_login(caller,user)
			return
	
	raise PermissionError("Denied to login.")

def succeed_login(caller,user):
	systemCS.executestring('notice "%s"' % escape("%s has logged in from %s as %s" % (formatCaller(caller), caller[0], user["username"])))
	UserSessionManager[caller]=(user["username"],user["privileges"])

@CSCommand("logout")
def logout(caller):
	del UserSessionManager[caller]
	playerCS.executeby(caller,"echo You have logged out.")

@CSCommand("whoami")
def whoami(caller,param=""):
	if param=="+login":
		return "%s - %s" % (str(caller),str(UserSessionManager[caller]))
	return str(caller)

@CSCommand("listusersessions","admin")
def listusersessions(caller):
	return str(UserSessionManager)