#!/usr/bin/env python

#string="+ 1 2"
string="+ (+ 4 3) (- 4 5) 2"

def parse():
	global string;
	output=[]
	
	while 1:
		print string
		if string.startswith("("):
			string=string[1:]
			output.append(parse())
		elif string.startswith(")"):
			string=string[1:]
			return output[:-1]
		
		elif string.startswith("["):
			pass
		elif string.startswith("\""):
			pass
		elif string.startswith(" "):
			output.append("")
			string=string[1:]
		elif string=="":
			break
		else:
			if len(output)==0:
				output.append("")
			output[-1],string=string[0],string[1:]
	return output

#print add(['1','2'])
print parse();
#print tokenize("(+ 1 (+ 2 3))");
#print parse(" spectator 1 1; spectator 0 1; test ")