#!/usr/bin/python



# MIT License
#
# Copyright (c) 2017 Beach Cities Software, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ___________________     _________       _____  __                                 
# \______   \_   ___ \   /   _____/ _____/ ____\/  |___  _  _______ _______   ____  
#  |    |  _/    \  \/   \_____  \ /  _ \   __\\   __\ \/ \/ /\__  \\_  __ \_/ __ \ 
#  |    |   \     \____  /        (  <_> )  |   |  |  \     /  / __ \|  | \/\  ___/ 
#  |______  /\______  / /_______  /\____/|__|   |__|   \/\_/  (____  /__|    \___  >
#         \/        \/          \/                                 \/            \/ 


#=======================================================
# Wrapper around RN2903 and RN2483 LoraWAN 
# modules' serial command interface from Microchip
# version: 0.1
# TODO: finish command set and functionality
# http://ww1.microchip.com/downloads/en/DeviceDoc/40001811A.pdf
#=======================================================

import serial
import time

# RN2903 and RN2483
class RN2XX3:
    TTYADDR = "/dev/ttyAMA0"
    BAUDRATE = 57600
    TIMEOUT = 5
    ser = 0
    CRLF = "\r\n"
    COMMANDS = {
        "SYS_VER":b"sys get ver" + CRLF,
        "SYS_VDD":b"sys get vdd" + CRLF,
        "SYS_HWEUI":b"sys get hweui" + CRLF,
        "SYS_NVMAT":b"sys get nvm {}" + CRLF,
        "SYS_SLEEP":b"sys sleep {}" + CRLF,
        "SYS_RST":b"sys reset" + CRLF,
        "SYS_NVMSET":b"sys set nvm {} {}" + CRLF,

        "MAC_DEVEUI":b"mac get deveui" + CRLF,
        }

    def init(self):
        self.ser = serial.Serial(self.TTYADDR, self.BAUDRATE, timeout=self.TIMEOUT)

    def getConn(self):
        return self.ser

    def closeConn(self):
        self.ser.close()

    def execCmd(self, cmd):
        print "Attempting to execute command: " + cmd
        self.ser.write(cmd)
        line = self.ser.readline()
        print "Command response: " + line + "\r\n"
        return line

    #=========================
    # SYS COMMANDS
    #=========================

    def getSysVersion(self):
        return self.execCmd(self.COMMANDS["SYS_VER"])

    def getSysVdd(self):
        return self.execCmd(self.COMMANDS["SYS_VDD"])

    def getSysHweui(self):
        return self.execCmd(self.COMMANDS["SYS_HWEUI"])

    def getSysNvmAt(self, nvmaddr):
        return self.execCmd(self.COMMANDS["SYS_NVMAT"].format(nvmaddr))

    def setSysNvmAg(self, nvmaddr, hexByte):
        return self.execCmd(self.COMMANDS["SYS_NVMSET"].format(nvmaddr, hexByte))

    def sysSleep(self, millis):
        return self.execCmd(self.COMMANDS["SYS_SLEEP"].format(millis))
    
    def sysReset(self):
        return self.execCmd(self.COMMANDS["SYS_RST"])

    #=========================
    # MAC COMMANDS
    #=========================

    def getMacDeveui(self):
        return self.execCmd(self.COMMANDS["MAC_DEVEUI"])

# end class

# test apparatus
def main():
    loraClient = RN2XX3()
    loraClient.init()
    print "\nCHIP FIRMWARE VERSION IS: " + loraClient.getSysVersion()
    time.sleep(1)
    print "\nCHIP HARDWARE EUI IS: " + loraClient.getSysHweui()
    time.sleep(1)
    print "\nCHIP VDD READING IS: " + loraClient.getSysVdd()
    time.sleep(1)
    print "\nCHIP MAC DEVEUI IS: " + loraClient.getMacDeveui()
    print "SLEEPING WITH RN2XX3 CHIP\r\n" + loraClient.sysSleep(3000)
    #print "SETTING NVM AT 3FF TO 88:" + loraClient.setSysNvmAg('3FF','88')
    time.sleep(0.25)
    print "\nNVM MEMORY VALUE AT: 3FF IS: " + loraClient.getSysNvmAt('3FF')
    #print "RESETTING CLIENT" + loraClient.sysReset()
    loraClient.closeConn()

if __name__ == "__main__":
    main()
