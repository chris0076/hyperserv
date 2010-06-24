"""Utility functions that do misc stuff(ex. convert between formats)"""
import struct, socket
import sbserver

def ipLongToString(num):
	return '%d.%d.%d.%d' % ((num & 0xff),
		(num >> 8) & 0xff,
		(num >> 16) & 0xff,
		(num >> 24) & 0xff)

def ipStringToLong(st):
	st = st.split('.')
	if len(st) != 4:
		raise ValueError('Not a valid ipv4 address')
	i = int(st[3])
	i = i << 8
	i = i | int(st[2])
	i = i << 8
	i = i | int(st[1])
	i = i << 8
	i = i | int(st[0])
	n = i
	if n > 0x7FFFFFFF:
		n = int(0x100000000 - n)
		if n < 2147483648:
			return -n
		else:
			return -2147483648
	return n

def formatOwner(owner):
	if owner[0]=="ingame":
		return sbserver.playerName(owner[1])
	if owner[0]=="irc":
		return "<irc> "+owner[1]
	return ""