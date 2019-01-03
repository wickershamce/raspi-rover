
""" Basic module to ease the use of pyOSC module https://trac.v2.nl/wiki/pyOSC

you must have pyOSC installed for this to run.

This is meant to be used by students or newies that are starting to experiment with OSC. If you are an advanced user
you probably want to bypass this module and use directly pyOSC, we have some examples of very simple use in our website.
Check the pyOSC website for more documentation.

License : LGPL

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
    
"""

try :
    from OSC import OSCServer, ThreadingOSCServer, ForkingOSCServer, OSCClient, OSCMessage, OSCBundle, getUrlStr
except :
    print "Warning!!! you must have pyOSC installed -> https://trac.v2.nl/wiki/pyOSC"
    
import threading

# client = iPhone
# server = raspbi

CLIENT_IP   = '192.168.1.200'
CLIENT_PORT = 9000 
SERVER_IP   = '192.168.1.201'
SERVER_PORT = 7000

client = 0
server = 0
st = 0


def printing_handler(addr, tags, data, source):
    print "---"
    print "received new osc msg from %s" % getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags :%s" % tags
    print "the actual data is : %s" % data
    print "---"



def initOSCClient(ip=CLIENT_IP, port=CLIENT_PORT) :
    global client
    client = OSCClient()
    client.connect( (ip,port) )
    
def initOSCServer(ip=SERVER_IP, port=SERVER_PORT, mode=0) :
    """ mode 0 for basic server, 1 for threading server, 2 for forking server
    """
    global server, st

    if mode == 0 :
        server = OSCServer( (ip ,port) ) # basic
    elif mode == 1 : 
        server = ThreadingOSCServer( (ip ,port) ) # threading
    elif mode == 2 :
        server = ForkingOSCServer( (ip ,port) ) # forking

    server.addDefaultHandlers()

def startOSCServer() :
    print "Registered Callback-functions are :"
    for addr in server.getOSCAddressSpace():
        print addr
    st = threading.Thread( target = server.serve_forever )
    st.start()

def setOSCHandler(address="/print", hd=printing_handler) :
    server.addMsgHandler(address, hd) # adding our function

def closeOSC() :
    if client is not 0 : client.close()
    if server is not 0 : server.close() 
    if st is not 0 : st.join()

def reportOSCHandlers() :
    print "Registered Callback-functions are :"
    for addr in server.getOSCAddressSpace():
        print addr
    
def sendOSCMsg( address='/print', data=[] ) :
    m = OSCMessage()
    m.setAddress(address)
    for d in data :
        m.append(d)
    client.send(m)

def createOSCBundle(address) : # just for api consistency
    return OSCBundle(address)
    
def sendOSCBundle(b):
    client.send(b)

def createOSCMsg(address='/print', data=[]) :
    m = OSCMessage()
    m.setAddress(address)
    for d in data :
        m.append(d)
    return m

################################################################################
# OSC callbacks
################################################################################

def cb_3xyM_lz(addr, tags, data, source):
    global speed1
    global speed2
    if data[0] == 0.0:
        # user released the joystick.
        sendOSCMsg('/3/xyM_l/', [0.5, 0.5]) # return stick to center
        speed1 = 0                          # stop motor 1
        speed2 = 0                          # stop motor 2
        print "joystick released"
    else:
        # user pressed the joystick
        pass

def cb_3xyM_l(addr, tags, data, source):

    # scale remote inputs
    dx = (data[1]-0.5)*2*255    # scales from 0-1 to -255 to 255
    dy = (data[0]-0.5)*2*255    # TODO add deadband
    
    # calculate motor speeds
    speed1 = dy + dx
    speed2 = dy - dx

    # constrain output to within PWM limits
    if speed1 >  255: speed1 =  255
    if speed1 < -255: speed1 = -255
    if speed2 >  255: speed2 =  255
    if speed2 < -255: speed2 = -255

    print "s1 = %i\t s2 = %i\t d1 = %.3f\t d2 = %.3f" % (speed1, speed2, data[0], data[1])
    
def cb_toggleB_2(addr, tags, data, source):
    global toggleB_2
    toggleB_2 = data[0]
    quit = data[0]
    print "quit pressed"
 
################################################################################
# Set up OSC client and server
################################################################################

# init client and server. do not use forking or threading for server
initOSCServer()
initOSCClient()

# bind event handler functions
setOSCHandler('/3/xyM_l/z', cb_3xyM_lz) 
setOSCHandler('/3/xyM_l', cb_3xyM_l)
setOSCHandler('/toggleB_2', cb_toggleB_2)

# start OSC server
startOSCServer()
print "Server started..."
