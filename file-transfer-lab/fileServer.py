#! /usr/bin/env python3

import sys, re, socket, os
sys.path.append("../lib")       # for params
import params
os.chdir("sFol")
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)

while True : 
    print("listening on:", bindAddr)

    sock, addr = lsock.accept()
    fork = os.fork() 
    if (fork == 0):
        print("connection rec'd from", addr)

        from framedSock import framedSend, framedReceive
        fName = framedReceive(sock, debug)     # Receive file name
        oFile = open(fName, "wb")
        while True:             # Once file transfer is done use system exit
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                break
            if b'%%e' in payload :
                oFile.close()       # closes file we're writing to
                sys.exit(0)
            oFile.write(payload)    # writes what is recieved aka payload to the file

     
