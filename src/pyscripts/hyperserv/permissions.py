#from hyperserv.events import eventHandler
import sbserver

class masterRequired(object):
	def __init__(self, func):
		self.func = func
		self.__doc__ = func.__doc__
		self.__name__ = func.__name__
	def __call__(self, *args):
		#try:
			#cn = args[0].cn
		#except AttributeError:
			#cn = args[0]
		owner=args[0].owner
		args=(owner,)+args[1:]
		if(owner[0]=="nobody"):
			return #log this
		self.func(*args)

class trustedRequired(object):
	def __init__(self, func):
		self.func = func
		self.__doc__ = func.__doc__
		self.__name__ = func.__name__
	def __call__(self, *args):
		#try:
			#cn = args[0].cn
		#except AttributeError:
			#cn = args[0]
		owner=args[0].owner
		args=(owner,)+args[1:]
		if(owner[0]=="nobody"):
			return #log this
		self.func(*args)

class adminRequired(object):
	def __init__(self, func):
		self.func = func
		self.__doc__ = func.__doc__
		self.__name__ = func.__name__
	def __call__(self, *args):
		#try:
			#cn = args[0].cn
		#except AttributeError:
			#cn = args[0]
		owner=args[0].owner
		args=(owner,)+args[1:]
		if(owner[0]=="nobody"):
			return #log this
		self.func(*args)