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
# TODO: finish command set and functionality, and add error checking, etc.
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
        "SYS_SLEEP":b"sys sleep {}" + CRLF,
        "SYS_RST":b"sys reset" + CRLF,
        "SYS_FACRST":b"sys factoryRESET" + CRLF,
        "SYS_ERASEFW":b"sys eraseFW" + CRLF,

        "SYS_VER":b"sys get ver" + CRLF,
        "SYS_VDD":b"sys get vdd" + CRLF,
        "SYS_HWEUI":b"sys get hweui" + CRLF,
        "SYS_NVMAT":b"sys get nvm {}" + CRLF,
        
        "SYS_NVMSET":b"sys set nvm {} {}" + CRLF,
        "SYS_PINCFG":b"sys set pindig {0} {1}" + CRLF,
        
        "MAC_RSTBAND":b"mac reset {}" + CRLF,
        "MAC_TX":b"mac tx {0} {1} {2}" + CRLF,
        "MAC_SAVE":b"mac save" + CRLF,
        "MAC_PAUSE":b"mac pause" + CRLF,
        "MAC_RESUME":b"mac resume" + CRLF,
        
        "MAC_DEVADDR":b"mac get devaddr" + CRLF,
        "MAC_DEVEUI":b"mac get deveui" + CRLF,
        "MAC_APPEUI":b"mac get appeui" + CRLF,
        "MAC_DR":b"mac get dr" + CRLF,
        "MAC_BAND":b"mac get band" + CRLF,
        "MAC_PWRIDX":b"mac get pwridx" + CRLF,
        "MAC_ADR":b"mac get adr" + CRLF,
        "MAC_RETX":b"mac get retx" + CRLF,
        "MAC_RXDELAY1":b"mac get rxdelay1" + CRLF,
        "MAC_RXDELAY2":b"mac get rxdelay2" + CRLF,
        "MAC_AR":b"mac get ar" + CRLF,
        "MAC_RX2":b"mac get rx2 {}" + CRLF,
        "MAC_DYCLEPS":b"mac get dcycleps" + CRLF,
        "MAC_MRGN":b"mac get mrgn" + CRLF,
        "MAC_GWNB":b"mac get gwnb" + CRLF,
        "MAC_STATUS":b"mac get status" + CRLF,

        "MAC_DEVADDRSET":b"mac set devaddr {}" + CRLF,
        "MAC_DEVEUISET":b"mac set deveui {}" + CRLF,
        "MAC_APPEUISET":b"mac set appeui {}" + CRLF,
        "MAC_NWKSKEYSET":b"mac set nwkskey {}" + CRLF,
        "MAC_APPSKEYSET":b"mac set appskey {}" + CRLF,
        "MAC_PWRIDXSET":b"mac set pwridx {}" + CRLF,
        "MAC_DRSET":b"mac set dr {}" + CRLF,
        "MAC_ADRSET":b"mac set adr {}" + CRLF,
        "MAC_BATSET":b"mac set bat {}" + CRLF,
        "MAC_RETXSET":b"mac set retx {}" + CRLF,
        "MAC_LINKCHKSET":b"mac set linkchk {}" + CRLF,
        "MAC_RXDELAY1SET":b"mac set rxdelay1 {}" + CRLF,
        "MAC_ARSET":b"mac set ar {}" + CRLF,
        "MAC_RXSET":b"mac set rx2 {0} {1}" + CRLF,
        

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
