"""This file contains the required functions for the editing features"""

import Image

import base
import cubes

from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

@CSCommand("loadimage","trusted")
def loadimage(caller,imagename,s=16,hf=1):
	s=int(s)
	hf=float(hf)
	im = Image.open(imagename)
	pixels = im.load()
	(xsize, ysize) = im.size
	for y in xrange(ysize):
		for x in xrange(xsize):
			h=int((sum(pixels[x,y])*hf)/3)
			print x,y,0,h,s
			cubes.makecolumn(caller,x,y,0,h,s)