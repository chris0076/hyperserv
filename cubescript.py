#!/usr/bin/env python
import re, random

class CSError(Exception): pass

class CSParser:
	def __init__(self, string):
		self.string=string
		self.quotefinder=re.compile('[^^]"')
	
	def consume(self,length=1):
		self.string=self.string[length:]

	def error(self,message):
		print message
		exit()

	def parse(self,expect=""):
		output=[""]
		
		while True:
			if self.string.startswith("("):
				self.consume()
				if not isinstance(output[-1], str):
					output.append("")
				output[-1]=self.parse(")")
			elif self.string.startswith(")"):
				if expect==")":
					self.consume()
					break
				else:
					raise CSError("Unexpected ): "+self.string)
			
			elif self.string.startswith("["):
				self.consume()
				if not isinstance(output[-1], str):
					output.append("")
				output[-1]=["lambda",""]
				output[-1][1]=self.parse("]")
			elif self.string.startswith("]"):
				if expect=="]":
					self.consume()
				else:
					raise CSError("Unexpected ]: "+self.string)
				break
			
			elif self.string.startswith("\""):
				try:
					position=self.quotefinder.search(self.string[1:]).start()+3
					output[-1]=self.string[1:position-1].replace('^"','"')
					self.consume(position)
					output.append("")
				except AttributeError:
					raise CSError("Unfinished \": "+self.string)
			
			elif self.string.startswith(" ") or self.string.startswith("\t"):
				self.consume()
				if output[-1]!="":
					output.append("")
			
			elif self.string.startswith(";") or self.string.startswith("\n"):
				self.consume()
				if output!=[""]:
					if output[-1]=="":
						output=output[:-1]
					output=["begin",output,self.parse()]
					if output[2]==[]:
						output=output[1]
			
			elif self.string.startswith("//"):
				self.string=self.string.partition("\n")[2]
			
			elif self.string=="":
				break
			else:
				if not isinstance(output[-1], str):
					output.append("")
				output[-1]=output[-1]+self.string[0]
				self.consume()
				
		if output[-1]=="":
			output=output[:-1]
		return output

class CSInterpreter:
		
	def __init__(self, command, outputfunction):
		self.command=command
		self.outputfunction=outputfunction
		
		self.functions = {
			"begin":  self.begin,
			"if":     self.csif,
			"loop":   self.csloop,
			"while":  self.cswhile,
			"+":      lambda params: self.numeric(sum,params),
			"-":      lambda params: self.numeric(lambda a: a[0]-a[1],params),
			"*":      lambda params: self.numeric(lambda a: reduce(lambda x,y: x*y,a),params),
			
			"=":      lambda params: self.numeric(lambda a: a[0]==a[1],params),
			"!=":     lambda params: self.numeric(lambda a: a[0]!=a[1],params),
			"<":      lambda params: self.numeric(lambda a: a[0]<a[1],params),
			">":      lambda params: self.numeric(lambda a: a[0]>a[1],params),
			"<=":     lambda params: self.numeric(lambda a: a[0]<=a[1],params),
			">=":     lambda params: self.numeric(lambda a: a[0]>=a[1],params),
			
			"div":    lambda params: self.numeric(lambda a: a[0]/a[1],params),
			"mod":    lambda params: self.numeric(lambda a: a[0]%a[1],params),
			"min":    lambda params: self.numeric(min,params),
			"max":    lambda params: self.numeric(max,params),
			
			"rnd":    lambda params: self.numeric(lambda a: random.randint(a[0],a[1]),params),
			"strcmp": lambda params: str(cmp(params[0],params[1])),
			"strstr": lambda params: str(params[0].find(params[1])),
			"strlen": lambda params: str(len(params[0])),
			"strstr": lambda params: str(params[0].find(params[1])),
			
			#ICOMMAND(rnd, "ii", (int *a, int *b), intret(*a - *b > 0 ? rnd(*a - *b) + *b : *b));
			#ICOMMAND(strcmp, "ss", (char *a, char *b), intret(strcmp(a,b)==0));
			#ICOMMAND(strstr, "ss", (char *a, char *b), { char *s = strstr(a, b); intret(s ? s-a : -1); });
			#ICOMMAND(strlen, "s", (char *s), intret(strlen(s)));
			
			"echo": self.echo
		}
		
		self.variables = {}
	
	def assignvar(self,name,value):
		self.variables[name]=value
		return value
	
	def numeric(self,function,params):
		string=str(function(map(int,params)))
		if string=="True":
			string="1"
		if string=="False":
			string="0"
		return string
	
	def force(self,params):
		if type(params) is list:
			if params[0]=="lambda":
				params=params[1]
		return self.execute(params)
	
	def begin(self,params):
		self.execute(params[0])
		return self.execute(params[1])
	
	def csif(self,params):
		if int(params[0]):
			return self.force(params[1])
		else:
			return self.force(params[2])
	
	def csloop(self,params):
		for i in range(0,int(params[1])):
			self.assignvar(params[0],i)
			self.force(params[2])
	
	def cswhile(self,params):
		while(int(self.force(params[0]))):
			self.force(params[1])
	
	def echo(self,params):
		self.outputfunction(' '.join(params))
	
	def execute(self,sexp):
		if type(sexp) != list:
			if type(sexp) is str and sexp.startswith("$"):
				#variable
				try:
					return str(self.variables[sexp[1:]])
				except KeyError:
					raise CSError("No such variable: "+sexp)
			#number/string
			return sexp
		try:
			#function
			if len(sexp)>1 and sexp[1]=="=":
				return self.assignvar(sexp[0],self.execute(sexp[2]))
			if sexp[0]=="lambda":
				return sexp
			return self.functions[sexp[0]](map(self.execute,sexp[1:]))
		except KeyError:
			raise CSError("No such command: "+sexp[0])
	def executestring(self):
		sexp=CSParser(self.command).parse()
		if type(sexp[0]) is list:
			sexp=sexp[0]
		self.execute(sexp)

if __name__ == '__main__':
	import readline
	def echo(msg):
		print msg
	while(1):
		CSInterpreter(raw_input(),echo).executestring()