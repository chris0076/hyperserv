from hypershade.config import config

if config["dbtype"]=="mysql":
	import MySQLdb as sqlmodule
elif config["dbtype"]=="sqlite":
	import sqlite3 as sqlmodule
else:
	raise Exception("Database driver %s not implemented." % config["dbtype"])

class HyperShadeDatabase():
	def __init__(self):
		if config["dbtype"]=="mysql":
			self.connection=sqlmodule.connect(host=config["dbhost"],user=config["dbuser"],passwd=config["dbpassword"],db=config["dbname"])
		elif config["dbtype"]=="sqlite":
			self.connection = sqlmodule.connect(config["dburl"])
			self.connection.text_factory = str
		self.cursor=self.connection.cursor()
	
	def query(self,*args):
		try:
			self.cursor.execute(*args)
		except sqlmodule.OperationalError:
			self.__init__() #reconnect to the server
			self.cursor.execute(*args)
		self.connection.commit()

database=HyperShadeDatabase()
