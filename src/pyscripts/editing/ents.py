"""This file contains the required functions for the editing features"""

import base
from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

editentnumber=base.packettypenumber("EDITENT")
editentlength=base.packettypes[editentnumber][1]
i=0
imax=10000
istart=1

@CSCommand("ent","trusted")
def entcommand(caller, *args):
	ent(args)

def ent(args):
	if len(args)==editentlength:
		j=args[0]
		args=args[1:]
	elif len(args)==editentlength-1:
		global i
		i+=1
		i%=imax
		j=i
	else:
		raise ServerError("EDITENT must have 9(if id is unspecified) or 10 arguments.")
	base.packetSendingQueue.put((editentnumber,j+istart)+args)
