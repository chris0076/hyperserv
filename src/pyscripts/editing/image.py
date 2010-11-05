"""This file contains the required functions for the editing features"""

import Image
import math

import base
import cubes

from hypershade.cubescript import playerCS, CSCommand
from hyperserv.servercommands import ServerError

@CSCommand("loadimage1","trusted")
def loadimage1(caller,imagename,s=16,maxh=20):
	s=int(s)
	(xsize, ysize, heights)=loadheightmap(imagename,int(maxh))
	
	mapsize=base.newmap(caller,math.ceil(max(math.log(xsize*s,2),math.log(ysize*s,2))))
	middleheight=2**(mapsize-1)/s
	
	for y in xrange(ysize):
		for x in xrange(xsize):
			cubes.makecolumn(caller,x,y,middleheight,heights[x][y],s)

@CSCommand("loadimage2","trusted")
def loadimage2(caller,imagename,s=16,maxh=20):
	s=int(s)
	(xsize, ysize, heights)=loadheightmap(imagename,int(maxh)*8)
	
	mapsize=base.newmap(caller,math.ceil(max(math.log(xsize*s,2),math.log(ysize*s,2))))
	middleheight=2**(mapsize-1)/s
	
	for y in xrange(ysize-1):
		for x in xrange(xsize-1):
			neighbourheights=(heights[y][x],heights[y][x+1],heights[y+1][x],heights[y+1][x+1])
			cubeheight=(max(neighbourheights)-1)/8+1
			cubes.makecolumn(caller,x,y,middleheight,cubeheight,s)
			cubes.corners(x,y,middleheight+cubeheight-1,(cubeheight*8-h for h in neighbourheights),s)

def loadheightmap(imagename,maxh):
	im = Image.open(imagename)
	pixels = im.load()
	(xsize, ysize) = im.size
	heights=[]
	for y in xrange(ysize):
		heights.append([])
		for x in xrange(xsize):
			heights[y].append(sum(pixels[x,y])*maxh/256/3)
	return xsize, ysize, heights