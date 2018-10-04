#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

print( "would you like to use stammer proxy or file server?" )

choice = input()

if (choice == "stammer proxy") :        # picks stammer proxy or file server depending on user input
    ipAd = "127.0.0.1:50000"
elif (choice == "file server") :
    ipAd = "127.0.0.1:50001"

switchesVarDefaults = (
    (('-s', '--server'), 'server', ipAd),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

print("Enter file name: ")
fileName = input()      # saves file name

try:
    oFile = open(fileName, "rb")        # opens file to read
    data = oFile.read()    

    framedSend(s, fileName.encode(), debug)     # sends file name to the server 


    i=0
    while i <= len(data):
        str = data[i:i+100]        # reads every 100 bytes
        framedSend(s, str, debug)   #sends every 100 bytes
        i+=100

    framedSend(s, b"%%e", debug)  # signal end of input
except (FileNotFoundError) :                # checks for files that do not exist
    print("Wrong file or file path")