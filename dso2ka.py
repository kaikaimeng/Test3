"""
Module name: dso2ka

Copyright:
----------------------------------------------------------------------
OpenWave-2KA is Copyright (c) 2014 Good Will Instrument Co., Ltd All Rights Reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You can receive a copy of the GNU Lesser General Public License from 
http://www.gnu.org/

Note:
OpenWave-2KA uses third party software which is copyrighted by its 
respective copyright holder. For details see the copyright notice 
of the individual package.

----------------------------------------------------------------------
Description:
Simple python module used to  get waveform and image from DSO.

Module imported:
  1. Python 2.7.3
  2. PySerial 2.7
  3. Matplotlib 1.3.1
  4. Numpy 1.8.0
  5. PIL 2.4.0

Version: 1.00

Created on MAY 15 2014

Author: Kevin Meng
"""
import serial
from serial.tools import list_ports
from PIL import Image
from struct import unpack
import numpy as np
import array
import struct
import sys,  time

__version__ = "1.00" #dso2ka module's version.

class Dso2ka:
    def __init__(self):
        global inBuffer
        self.ver=__version__ #Driver version.
        self.sWave=[[], []]
        self.fWave=[[], []]
        self.vdiv=[[], []]   #Kevin 2014.04.21
        self.vunit=[[], []]  #Kevin 2014.04.21
        self.dt=[[], []]
        self.vpos=[[], []]
        self.hpos=[[], []]
        self.ch_list=[]
        self.info=[[], []]
    def ScanComPort(self):
        port_list=list(list_ports.comports())
        num=len(port_list)
        print num
        for i in xrange(num):
            str=port_list[i][2].split('=')
            if(str[0]=='USB VID:PID'):
                str=str[1].split(' ')[0] #Extract VID and PID from string.
                str=str.split(':')
                print str
                if((str[0]=='2184')and((str[1]=='0013')or(str[1]=='0014')or(str[1]=='0022')or(str[1]=='0023'))):
                    port=port_list[i][0]
                    print port
                    self.IO = serial.Serial(port, baudrate=384000, bytesize=8, parity ='N', stopbits=1, xonxoff=False, dsrdtr=False, timeout=10)
                    time.sleep(0.5)
                    while(True):
                        num=self.IO.inWaiting()
                        if(num==0):
                            break
                        else:
                            print '-',
                        self.IO.flushInput()              #Clear input buffer.
                        time.sleep(0.1)
                            
                    self.write('*IDN?\n')
                    name = self.read().split(',')         #Query *IDN?
                    print('%s connected!\n'% name[1])     #Print model name.
                    return 0
        print('Device not found!')
        return -1
        
    def write(self, str):
        self.IO.write(str)
        
    def read(self):
        return self.IO.readline()
    
    def getBlockData(self): #Used to get image data.
        global inBuffer
        inBuffer=self.IO.read(10)
        length=len(inBuffer)
        self.headerlen = 2 + int(inBuffer[1])
        pkg_length = int(inBuffer[2:self.headerlen]) + self.headerlen + 1 #Block #48000[..8000bytes raw data...]<LF>
        print "Data transferring...  (%d bytes)" % pkg_length

        pkg_length=pkg_length-length
        while True:
            #print(pkg_length)
            if(pkg_length > 100000):
                buf=self.IO.read(100000)
                num=len(buf)
                inBuffer+=buf
                pkg_length=pkg_length-num
            else:
                buf=self.IO.read(pkg_length)
                num=len(buf)
                inBuffer+=buf
                pkg_length=pkg_length-num
                if(pkg_length==0):
                    break
        #print("%d bytes received!" % len(data))
        #print("Package len: %d" % self.headerlen)
        #print("data len: %d" % len(data))

    def RleDecode(self):
        raw_data=[]
        #Convert 8 bits array to 16 bits array.
        data = np.array(unpack('<%sh' % (len(inBuffer[self.headerlen:-1])/2), inBuffer[self.headerlen:-1]))
        l=len(data)
        if( l%2 != 0):   #Ignore reserved data.
            l=l-1
        #print(l)
        package_length=len(data)
        #print(package_length)
        index=0
        bmp_size=0
        while True:
            length =data[index]
            value =data[index+1]
            index+=2
            bmp_size+=length
            buf=[ value for x in range(0,length)]
            raw_data+=buf
            if(index>=l):
                break
        #print len(raw_data)
        width = 800
        height = 600
        self.im = Image.new("RGB", (width, height))

        #Convert from rgb565 into rgb888
        index=0
        for y in xrange(height):
            for x in xrange(width):
                px = raw_data[index]
                self.im.putpixel((x, y),((px & 0xF800) >> 8, (px & 0x07E0) >> 3, (px & 0x001F) << 3))
                index += 1

    def getRawData(self, header_on,  ch): #Used to get waveform's raw data.
        print('waiting CH%d data... ' % ch)
        if(header_on==True):
            self.IO.write(":HEAD ON\n")
        else:
            self.IO.write(":HEAD OFF\n")

        if(self.checkAcqState(ch)== -1):
            return
        self.IO.write(":ACQ%d:MEM?\n" % ch)                    #Write command(get raw datas) to DSO.
        print('Reading CH%d data...' % ch)

        if(header_on == True):
            index=len(self.ch_list)
            if(index==0): #Getting first waveform => reset self.info.
                self.info=[[], []]
            #print(index)
            self.info[index]=self.IO.readline().split(';')
            num=len(self.info[index])
            self.info[index][num-1]=self.info[index][num-2] #Convert info[] to csv compatible format.
            self.info[index][num-2]='Mode,Fast'
            #print num, self.info[index]
            sCh = [s for s in self.info[index] if "Source" in s]
            self.ch_list.append(sCh[0].split(',')[1])
            sDt = [s for s in self.info[index] if "Sampling Period" in s]
            self.dt[index]=float(sDt[0].split(',')[1])
            sDv = [s for s in self.info[index] if "Vertical Scale" in s]
            self.vdiv[index]=float(sDv[0].split(',')[1]) #Kevin 2014.04.21
            sVpos=[s for s in self.info[index] if "Vertical Position" in s] #Kevin 2014.04.21
            self.vpos[index]=float(sVpos[0].split(',')[1])
            sHpos = [s for s in self.info[index] if "Horizontal Position" in s]
            self.hpos[index]=float(sHpos[0].split(',')[1])
            sVunit=[s for s in self.info[index] if "Vertical Units" in s] #Kevin 2014.04.21
            self.vunit[index]=sVunit[0].split(',')[1]
            #print sHpos, self.vdiv[index],  self.dt[index],  self.hpos[index], sDv
        self.getBlockData()
        #print('CH List: %s' %self.ch_list)
        return index #Return the buffer index.
        #print("%d bytes received!" % len(self.Waveform))
        #print("Package len: %d" % self.headerlen)
        #print("self.Waveform len: %d" % len(self.Waveform))

    def checkAcqState(self,  ch):
        str_stat=":ACQ%d:STAT?\n" % ch
        loop_cnt = 0
        max_cnt=0
        while True:                                #Checking acquisition is ready or not.
            self.IO.write(str_stat)
            state=self.IO.readline()
            if(state[0] == '1'):
                break
            time.sleep(0.1)
            loop_cnt +=1
            if(loop_cnt >= 50):
                print('Please check signal!')
                loop_cnt=0
                max_cnt+=1
                if(max_cnt==5):
                    #print('Abort CH%d reading.' % ch)
                    #Checking abort key pressed!
                    return -1
        return 0

    def constructWaveform(self,  index):
        self.points_num=len(inBuffer[self.headerlen:-1])/2   #Calculate sample points length.
        #print(self.points_num)
        self.sWave[index] = np.array(unpack('>%sh' % (len(inBuffer[self.headerlen:-1])/2), inBuffer[self.headerlen:-1])) #Kevin 2014.04.11
        self.fWave[index]=[0]*self.points_num #Kevin 2014.03.27
        dv=self.vdiv[index]/25 #Kevin 2014.04.21
        for x in range(self.points_num):           #Convert 16 bits signed to floating point number.
            self.fWave[index][x]=float(self.sWave[index][x])*dv #Kevin 2014.04.21

    def readRawDataFile(self,  fileName):
        #Check file format(csv or lsf)
        if(fileName.lower().endswith('.csv')):
            self.dataType='csv'
        elif(fileName.lower().endswith('.lsf')):
            self.dataType='lsf'
        else:
            return -1
        f = open(fileName, 'r')
        info=[]
        #Read file header.
        if(self.dataType=='csv'):
            for x in xrange(26):
                info.append(f.readline().split(',\n')[0])
            #print len(info), info
            #print info[0]
            if(info[0].split(',')[1]!='2.0A'): #Check format version
                f.close()
                return -1
            count=info[5].count('CH')  #Check channel number in file.
            wave=f.read().splitlines() #Read raw data from file.
            self.points_num=len(wave)
            #print('count= %d'% count)
        else:
            info=f.readline().split(';') #The last item will be '\n'.
            #print len(info),  info
            if(info[0].split('Format,')[1]!='2.0A'): #Check format version
                f.close()
                return -1
            if(f.read(1)!='#'):
                sys.exit(0)
            digit=int(f.read(1))
            num=int(f.read(digit))
            #print('lsf num: %d'%num)
            count=info[5].count('CH') #Check channel number in file(should be 1 here).
            wave=f.read() #Read raw data from file.
            self.points_num=len(wave)/2   #Calculate sample points length.
            #print(dso.points_num)
        f.close()
        #print('length %d' % self.points_num)
        #write first waveform's info to self.info[0]
        #
        self.info=[[], []]
        if(count==1): #1 channel
            self.sWave[0]=[0]*self.points_num
            self.fWave[0]=[0]*self.points_num
            self.ch_list.append(info[5].split(',')[1])
            self.vunit[0] =info[6].split(',')[1] #Get vertical units. Kevin 2014.04.21
            self.vdiv[0]   = float(info[12].split(',')[1]) #Get vertical scale. => Voltage for ADC's single step.  Kevin 2014.04.21
            self.vpos[0] =float(info[13].split(',')[1]) #Get vertical position.
            self.hpos[0] =float(info[16].split(',')[1]) #Get horizontal position.
            self.dt[0]   =float(info[19].split(',')[1]) #Get sample period.
            dv1=self.vdiv[0]/25 #Kevin 2014.04.21
#            pos=self.vpos[0]/self.dv[0]
#            print('pos=%f, vpos=%d' %(pos, int(pos)))
            vpos=int(self.vpos[0]/dv1)+128 #Kevin 2014.04.21
            vpos1=self.vpos[0]
            if(self.dataType=='csv'):
                for x in xrange(26):
                    self.info[0].append(info[x])
                for x in xrange(self.points_num):
                    value=int(wave[x].split(',')[0])
                    self.sWave[0][x]=value
                    self.fWave[0][x]=value*dv1
            else: #lsf file
                for x in xrange(24):
                    self.info[0].append(info[x])
                self.info[0].append('Mode,Fast') #Convert info[] to csv compatible format.
                self.info[0].append(info[24])
                self.sWave[0] = np.array(unpack('<%sh' % (len(wave)/2), wave))
                for x in range(self.points_num):                #Convert 16 bits signed to floating point number.
                    self.sWave[0][x]-=vpos
                    self.fWave[0][x]=float(self.sWave[0][x])*dv1 #Kevin 2014.04.15
                #Change info[] to csv compatible format.
                #print len(self.info[0]), self.info[0]
            return 1
        elif(count==2): #2 channel, csv file only.
            #write waveform's info to self.info[]
            self.info[0].append(info[0])
            self.info[1].append(info[0])
            for x in xrange(1, 26):
                str=info[x].split(',')
                self.info[0].append('%s,%s'%(str[0],  str[1]))
                self.info[1].append('%s,%s'%(str[2],  str[3]))
            self.ch_list.append(info[5].split(',')[1])
            self.sWave[0]=[0]*self.points_num
            self.fWave[0]=[0]*self.points_num
            self.vunit[0] =info[6].split(',')[1] #Get vertical units. Kevin 2014.04.21
            self.vdiv[0]    = float(info[12].split(',')[1]) #Get vertical scale. => Voltage for ADC's single step.  Kevin 2014.04.21
            self.vpos[0] =float(info[13].split(',')[1]) #Get vertical position.
            self.hpos[0] =float(info[16].split(',')[1]) #Get horizontal position.
            self.dt[0]     =float(info[19].split(',')[1]) #Get sample period.
            self.ch_list.append(info[5].split(',')[3])
            self.sWave[1]=[0]*self.points_num
            self.fWave[1]=[0]*self.points_num
            self.vunit[1] =info[6].split(',')[1] #Get vertical units. Kevin 2014.04.21
            self.vdiv[1]    = float(info[12].split(',')[3]) #Get vertical scale. => Voltage for ADC's single step.  #Kevin 2014.04.21
            self.vpos[1] =float(info[13].split(',')[3]) #Get vertical position.
            self.hpos[1] =float(info[16].split(',')[3]) #Get horizontal position.
            self.dt[1]     =float(info[19].split(',')[3]) #Get sample period.
            dv1=self.vdiv[0]/25  #Kevin 2014.04.21
            dv2=self.vdiv[1]/25  #Kevin 2014.04.21
            #print('dv1=%f, dv2=%f' %(dv1,  dv2))
            for i in xrange(self.points_num):
                value=int(wave[i].split(',')[0])
                self.sWave[0][i]=value
                self.fWave[0][i]=value*dv1
                value=int(wave[i].split(',')[2])
                self.sWave[1][i]=value
                self.fWave[1][i]=value*dv2
            return 2
        else:
            return -1

