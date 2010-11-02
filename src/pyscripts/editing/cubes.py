"""This file contains the required functions for the editing features"""

import editing
from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

@CSCommand("editf","trusted")
def editf(caller,*args):
	editing.sendpacket("EDITF",*args)

@CSCommand("makecube","trusted")
def makecube(caller,x,y,z,s=16):
	s=int(s)
	x=int(x)*s
	y=int(y)*s
	z=int(z)*s
	editf(caller,x+s,y,z,1,1,1,s,0,0,2,0,2,1,-1,1)

@CSCommand("makecolumn","trusted")
def makecolumn(caller,x,y,z=0,h=16,s=16):
	s=int(s)
	h=int(h)
	x=int(x)*s
	y=int(y)*s
	z=int(z)*s
	editf(caller,x+s,y,z,1,1,h,s,0,0,2,0,2,1,-1,1)