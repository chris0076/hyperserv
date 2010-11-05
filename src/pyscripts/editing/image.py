"""This file contains the required functions for the editing features"""

import Image

import base
import cubes

from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

@CSCommand("loadimage1","trusted")
def loadimage1(caller,imagename,s=16,hf=0.15):
	s=int(s)
	hf=float(hf)
	im = Image.open(imagename)
	pixels = im.load()
	(xsize, ysize) = im.size
	for y in xrange(ysize):
		for x in xrange(xsize):
			cubes.makecolumn(caller,x,y,0,int((sum(pixels[x,y])*hf)/3),s)

@CSCommand("loadimage2","trusted")
def loadimage1(caller,imagename,s=16,hf=0.5):
	s=int(s)
	hf=float(hf)
	im = Image.open(imagename)
	pixels = im.load()
	(xsize, ysize) = im.size
	
	heights=[]
	for y in xrange(ysize):
		heights.append([])
		for x in xrange(xsize):
			heights[y].append(int((sum(pixels[x,y])*hf)/3))
			
	for y in xrange(ysize-1):
		for x in xrange(xsize-1):
			neighbourheights=(heights[y][x],heights[y][x+1],heights[y+1][x],heights[y+1][x+1])
			cubeheight=max(neighbourheights)
			cubes.makecolumn(caller,x,y,0,cubeheight/8,s)
			cubes.corners(x,y,cubeheight/8-1,(cubeheight-x for x in neighbourheights),s)