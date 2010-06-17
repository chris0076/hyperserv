#!/usr/bin/env python

from sexpr import str2sexpr

#def multisplit(s, seps):
	#"""Splits with multiple separators"""
	#res = [s]
	#for sep in seps:
		#s, res = res, []
		#for seq in s:
			#res += seq.split(sep)
	#return res

#def parse(command):
	#command=command.strip();
	#instructions=command.split(";")
	#if(command==""):
		#return ""
	##elif (command=="")
	#return instructions;
	
	#return ""

def tokenize(command):
	tokens=[]
	command=command.strip(" ")
	while(command!=""):
		if(command[0]=="("):
			partition=command.partition(")")
			tokens.append(partition[0][1:])
			command=command[2]
		elif(command[0]=="["):
			partition=command.partition("]")
			tokens.append(partition[0][1:])
			command=command[2]
		elif(command[0]=="\""):
			partition=command.partition("\"")
			tokens.append(partition[0][1:])
			command=command[2]
		else:
			partition=command.partition(" ")
			tokens.append(partition[0])
			command=command[2]
		command=command.strip(" ")
	return tokens

def parse(command):
	#Split into tokens
	if command[0]=="(":
		if command[-1]!=")":
			print "Expected )"
		else:
			command=command[1:-1]
	if command[0]=="[":
		if command[-1]!="]":
			print "Expected ]"
		else:
			command=command[1:-1]
	tokens=command.split();
	
	#prepare
	function,parameters=tokens[0],tokens[1:]
	
	#make sure everything is redox
	for i in range(0,len(parameters)):
		if parameters[i].startswith("(") or parameters[i].startswith("["):
			parameters[i]=parse(parameters[i])
	
	#do the function
	if(function=="+"):
		return add(parameters)
	else: print "Unknown function "+function
	return 0

def add(parameters):
	return sum(map(int,parameters));

print str2sexpr("(+ 1; + 1 2 [+ 3 4])")

#print add(['1','2'])
#print parse("(+ 1 2)");
#print tokenize("(+ 1 (+ 2 3))");
#print parse(" spectator 1 1; spectator 0 1; test ")