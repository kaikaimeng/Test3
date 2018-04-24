"""
Program name: gds2kaSnProgrammer

Copyright:
----------------------------------------------------------------------
gds3kProg is Copyright (c) 2014 Good Will Instrument Co., Ltd All Rights Reserved.

Module imported:
  1. Python 2.7.6
  2. dso 1.00
  3. PySerial 2.7
  4. Matplotlib 1.3.1
  5. Numpy 1.8.0
  6. PySide 1.2.1

Version: 1.00

Created on SEP 25 2017

Author: Kevin Meng

Test3
111

"""

import os, sys, time
import dso2ka, dso2ke

__version__ = "1.00" #OpenWave-3K software version.


    
#H cursor test----------------------------------------------------------------------
def HCursorTest():
    #Set H position to 0.
    str=':TIM:POS 0\n'
    print str
    dso.write(str)

    #Get H scale.
    str=':TIM:SCAL?\n'
    print str
    dso.write(str)
    hscale=dso.read().split('\n')[0]
    print hscale, '\n'
    
    #Set cursor mode to H cursor.
    str='CURS:MOD H\n'
    print str
    dso.write(str)
    
    #Set H cursor tracking off.
    str=':CURS:HTRAC OFF\n'
    print str
    dso.write(str)

    #Get H cursor tracking state.
    str=':CURS:HTRAC?\n'
    print str
    dso.write(str)
    ss=dso.read()
    print ss

    #Set H1 initial position
    str=':CURS:H1P -%s\n'%hscale
    print str
    dso.write(str)

    #Set H2 initial position
    str=':CURS:H2P %s\n'%hscale
    print str
    dso.write(str)
    
    #Get H1 Cursor position.
    str=':CURS:H1P?\n'
    print str
    dso.write(str)
    h1pos=float(dso.read())
    print h1pos
    
    #Get H2 Cursor position.
    str=':CURS:H2P?\n'
    print str
    dso.write(str)
    h2pos=float(dso.read())
    print h2pos

    time.sleep(0.5)
    
    #Move H1 position
    for i in xrange(1,6,1):  #from 1 below 6, step: 1
        str=':CURS:H1P %e\n'%(h1pos-i*float(hscale))
        print str
        dso.write(str)
        time.sleep(0.5)

    #Move H2 position
    for i in xrange(1,6,1):  #from 1 below 6, step: 1
        str=':CURS:H2P %e\n'%(h2pos-i*float(hscale))
        print str
        dso.write(str)
        time.sleep(0.5)

    #Get H1 Cursor position.
    str=':CURS:H1P?\n'
    print str
    dso.write(str)
    h1pos=float(dso.read())
    print h1pos

    #Get H2 Cursor position.
    str=':CURS:H2P?\n'
    print str
    dso.write(str)
    h2pos=float(dso.read())
    print h2pos
    
    #Set H Cursor tracking on.
    str=':CURS:HTRAC ON\n'
    print str
    dso.write(str)

    #Get H cursor tracking state.
    str=':CURS:HTRAC?\n'
    print str
    dso.write(str)
    ss=dso.read()
    print ss

    #Move H1 position
    for i in xrange(1,6,1):  #from 1 below 6, step: 1
        str=':CURS:H1P %e\n'%(h1pos+i*float(hscale))
        print str
        dso.write(str)
        time.sleep(0.5)

    #Get H1 Cursor position.
    str=':CURS:H1P?\n'
    print str
    dso.write(str)
    h1pos=float(dso.read())
    print h1pos

    #Get H2 Cursor position.
    str=':CURS:H2P?\n'
    print str
    dso.write(str)
    h2pos=float(dso.read())
    print h2pos

    #Set H cursor tracking off.
    str=':CURS:HTRAC OFF\n'
    print str
    dso.write(str)

    #Get H cursor tracking state.
    str=':CURS:HTRAC?\n'
    print str
    dso.write(str)
    ss=dso.read()
    print ss
#V cursor test--------------------------------------------------------------
def VCursorTest():
    #Set cursor source.
    str=':CURS:SOUR CH1\n'
    print str
    dso.write(str)

    #Set CH1 vertical position to 0.
    str=':CHAN1:POS 0\n'
    print str
    dso.write(str)

    #Get CH1 vertical scale.
    str=':CHAN1:SCAL?\n'
    print str
    dso.write(str)
    v1scale=dso.read().split('\n')[0]
    print v1scale, '\n'
    
    #Set cursor mode to HV cursor.
    str='CURS:MOD HV\n'
    print str
    dso.write(str)
    
    #Set V cursor tracking off.
    str=':CURS:VTRAC OFF\n'
    print str
    dso.write(str)

    #Get V cursor tracking state.
    str=':CURS:VTRAC?\n'
    print str
    dso.write(str)
    ss=dso.read()
    print ss
    
    #Set V1 initial position
    str=':CURS:V1P %s\n'%v1scale
    print str
    dso.write(str)

    #Set V2 initial position
    str=':CURS:V2P -%s\n'%v1scale
    print str
    dso.write(str)
    
    #Get V1 Cursor position.
    str=':CURS:V1P?\n'
    print str
    dso.write(str)
    v1pos=float(dso.read())
    print v1pos
    
    #Get V2 Cursor position.
    str=':CURS:V2P?\n'
    print str
    dso.write(str)
    v2pos=float(dso.read())
    print v2pos

    time.sleep(0.5)
    
    #Move V1 position
    for i in xrange(1,4,1):  #from 1 below 4, step: 1
        str=':CURS:V1P %e\n'%(v1pos+i*float(v1scale))
        print str
        dso.write(str)
        time.sleep(0.5)
    
    #Move V2 position
    for i in xrange(1,4,1):  #from 1 below 4, step: 1
        str=':CURS:V2P %e\n'%(v2pos+i*float(v1scale))
        print str
        dso.write(str)
        time.sleep(0.5)
    
    #Get V1 Cursor position.
    str=':CURS:V1P?\n'
    print str
    dso.write(str)
    v1pos=float(dso.read())
    print v1pos

    #Get V2 Cursor position.
    str=':CURS:V2P?\n'
    print str
    dso.write(str)
    v2pos=float(dso.read())
    print v2pos

    time.sleep(0.5)
    
    #Set V Cursor tracking on.
    str=':CURS:VTRAC ON\n'
    print str
    dso.write(str)
    
    #Get V cursor tracking state.
    str=':CURS:VTRAC?\n'
    print str
    dso.write(str)
    ss=dso.read()
    print ss
        
    #Move V1 position
    for i in xrange(1,3,1):  #from 1 below 3, step: 1
        str=':CURS:V1P %e\n'%(v1pos-i*float(v1scale))
        print str
        dso.write(str)
        time.sleep(0.5)

    #Get V1 Cursor position.
    str=':CURS:V1P?\n'
    print str
    dso.write(str)
    v1pos=float(dso.read())
    print v1pos
    
    #Get V2 Cursor position.
    str=':CURS:V2P?\n'
    print str
    dso.write(str)
    v2pos=float(dso.read())
    print v2pos

    time.sleep(0.5)
    
    #Move V2 position
    for i in xrange(1,5,1):  #from 1 below 5, step: 1
        str=':CURS:V2P %e\n'%(v2pos-i*float(v1scale))
        print str
        dso.write(str)
        time.sleep(0.5)

    #Get V2 Cursor position.
    str=':CURS:V2P?\n'
    print str
    dso.write(str)
    v2pos=float(dso.read())
    print v2pos

    #Set V cursor tracking off.
    str=':CURS:VTRAC OFF\n'
    print str
    dso.write(str)

    #Get V cursor tracking state.
    str=':CURS:VTRAC?\n'
    print str
    dso.write(str)
    ss=dso.read()
    print ss



#500us/div, set H2 to 500us. And then read H2 position will be 495us.  It's a bug.
def cursorPosTest():
    #Set H position to 0.
    str=':TIM:POS 0\n'
    print str
    dso.write(str)

    #Get H scale.
    str=':TIM:SCAL?\n'
    print str
    dso.write(str)
    hscale=dso.read().split('\n')[0]
    print hscale, '\n'
    
    #Set cursor mode to H cursor.
    str='CURS:MOD H\n'
    print str
    dso.write(str)
    
    #Set H cursor tracking off.
    str=':CURS:HTRAC OFF\n'
    print str
    dso.write(str)
    
    #Set H1 initial position
    str=':CURS:H1P -%s\n'%hscale
    print str
    dso.write(str)

    #Set H2 initial position
    str=':CURS:H2P %s\n'%hscale
    print str
    dso.write(str)
    
    #Get H1 Cursor position.
    str=':CURS:H1P?\n'
    print str
    dso.write(str)
    h1pos=float(dso.read())
    print h1pos
    
    #Get H2 Cursor position.
    str=':CURS:H2P?\n'
    print str
    dso.write(str)
    h2pos=float(dso.read())
    print h2pos


if __name__ == '__main__':
    global portNum

    print('-----------------------------------------------------------------------------');
    print('This program is used to test the gated measurement by remote command.\n')
    print('-----------------------------------------------------------------------------');
    dso=dso2ka.Dso2ka()
#    dso=dso2ke.Dso2ke()

    #Search and make a connection with COM port.
    portNum=dso.ScanComPort() #Scan COM port.
    
    if(portNum == -1):
        print('DSO not found, please connect USB cable and try again!')
        raw_input('Press "Enter" to Exit!')
        sys.exit(0)

    dso.write('*IDN?\n')
    name = dso.read().split(',')         #Query *IDN?
    print name

    HCursorTest()
    time.sleep(0.5)
    VCursorTest()

