"""
	Utils.py -- Utility Functions
	
	Sources of code:
		Eloipool - Python Bitcoin pool server by 
		Copyright (C) 2011-2012  Luke Dashjr <luke-jr+eloipool@utopios.org>
	
	extra code by elchupa
"""
from hashlib import sha256
from struct import unpack

def swap32(b):
	o = b''
	for i in range(0, len(b), 4):
		o += b[i + 3:i - 1 if i else None:-1]
	return o

def sha2x( data ):
	return sha256( sha256( data ).digest() ).digest() 	

def sha2int(h):
	n = unpack('<QQQQ', h)
	n = (n[3] << 192) | (n[2] << 128) | (n[1] << 64) | n[0]
	return n
