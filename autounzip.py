#!/usr/bin/env python

'''
This is a script for automatically unzipping a repeatedly compressed file. 
Prints the contents of the file to stdout using cat when ASCII is detected.
WARNING: DESTRUCTIVE --- Make a copy of the starting file before running.
TODO --- Add clauses for more zip formats: 7z, etc.
'''
from pwn import *

s = ssh('bandit12', 'bandit.labs.overthewire.org', 2220, '5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu')

#Generate and cd to a temporary working directory
start = '/home/bandit12'
cwd = s.set_working_directory()

#Copy file to newly created temp directory

io = s.process('/bin/bash', env={"PS1:":""})
io.sendline('cp %s/data.txt data.txt' % start)
io.sendline('xxd -r data.txt newdata')
io.sendline('rm data.txt')

for i in xrange(100):
	io.sendline('ls')
	theList = io.recvline()
	fileName = theList.strip().split(' ')[-1]
	io.sendline('file *')
	theType = io.recvline()
	if 'gzip' in theType:
		line = 'mv %s %d.gz' % (fileName, i)
		io.sendline(line)
		line = 'gunzip %d.gz' % i
		io.sendline(line)
	elif 'bzip2' in theType:
		line = 'bunzip2 %s' % fileName
		io.sendline(line)
		io.recvline()
	elif 'tar' in theType:
		line = 'tar xvf %s' % fileName
		io.sendline(line)
		io.recvline()
		line = 'rm %s' % fileName
		io.sendline(line)
	elif 'ASCII' in theType:	
		io.sendline('cat %s' % fileName)
		print io.recvline();
		s.close()	
		break
