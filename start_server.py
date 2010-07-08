#!/usr/bin/env python
import os, sys

hyperserv_root_path = ''
pyscripts_path = ''
hyperserv_bin_path = ''

cwddirs = os.getcwd().split('/')
root_found = False

if hyperserv_root_path == '':
	for dir in cwddirs:
		if dir.find('hyperserv') > -1:
			root_found = True
		hyperserv_root_path += dir + '/'
else:
	root_found = True

if not root_found:
	print 'Error: Could not find XSBS root in your current path.'
	print 'Please cd into the XSBS source directory and re-run this script.'
	sys.exit(1)

if pyscripts_path == '':
	pyscripts_path = hyperserv_root_path + 'src/pyscripts'
if not os.path.isdir(pyscripts_path):
	print 'Error: Could not find pyscripts folder in your XSBS directory.'
	print 'Did you perform an out of source build?  Make sure you are in the XSBS source directory.'
	sys.exit(1)

def start():
	global hyperserv_bin_path
	if hyperserv_bin_path == '':
		hyperserv_bin_path = hyperserv_root_path + 'src/hyperserv'
	if not os.path.isfile(hyperserv_bin_path):
		os.execlpe('hyperserv', 'hyperserv', '-lsauer.log', '-s'+pyscripts_path, os.environ)
	else:
		os.execle(hyperserv_bin_path, 'hyperserv' '-lsauer.log', '-s'+pyscripts_path, os.environ)

try:
	start()
except OSError:
	print "Maybe not compiled, Compiling:"
	print os.popen('cmake .').read()
	print os.popen('make').read()
	start()