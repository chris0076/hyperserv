#!/usr/bin/env python
import re

#string="+ 1 2"
string='+ (+ 433   [+ 1 "alex test  //test"] 9 3) (- 4 5 ) 2'

string="""
if $blendpaintmode [scrollblendbrush $arg1
] [
editfacewentpush $arg1 1 // Fill and Empty cube
]
"""

quotefinder=re.compile("\"")

def consume(length=1):
	global string
	string=string[length:]

def parse():
	global string
	output=[""]
	
	while True:
		print string
		print "output", output
		if string.startswith("("):
			consume()
			if not isinstance(output[-1], str):
				output.append("")
			output[-1]=parse()
		elif string.startswith(")"):
			consume()
			break
		
		elif string.startswith("["):
			consume()
			if not isinstance(output[-1], str):
				output.append("")
			output[-1]=["lambda",""]
			output[-1][1]=parse()
		elif string.startswith("]"):
			consume()
			break
		
		elif string.startswith("\""):
			position=quotefinder.search(string[1:]).start()+2
			output[-1]=string[:position]
			consume(position)
		
		elif string.startswith(" ") or string.startswith("\t"):
			consume()
			if output[-1]!="":
				output.append("")
		
		elif string.startswith(";") or string.startswith("\n"):
			consume()
			if output!=[""]:
				if output[-1]=="":
					output=output[:-1]
				output=["begin",output,parse()]
				if output[2]==[]:
					output=output[1]
		
		elif string.startswith("//"):
			string=string.partition("\n")[2]
		
		elif string=="":
			break
		else:
			if not isinstance(output[-1], str):
				output.append("")
			output[-1]=output[-1]+string[0]
			consume()
			
	if output[-1]=="":
		output=output[:-1]
	return output

#print add(['1','2'])
print parse();
#print tokenize("(+ 1 (+ 2 3))");
#print parse(" spectator 1 1; spectator 0 1; test ")