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

# version: 0.1 changes
# - Interface to the RN2903 and RN2483 LoraWAN modules using a standard serial command interface
#
# TODO: finish command set and functionality, and add error checking, etc.
# http://ww1.microchip.com/downloads/en/DeviceDoc/40001811A.pdf

# version 0.2 changes, July 6, 2018, github@rolandvs
# (1)   as all commands have a `CRLF` added, it is worth putting it in the write function
#       instead of adding it at every command.
# (2)   as we support more than just `serial` we moved it out of the class
# (3)   debug messages are suppressed or shown using verbose= when creating an instance of the class
#
# When using with micropython the selected UART(2) and speed(57600) can be changed in function main().
# When importing the class in another program, create a serial port for your system and pass it to the
# class.
#
# RN2483
# 1 GND
# 2 RTS -- not connected
# 3 CTS -- not connected
# 6 TXD -> PA1-RX-UART4
# 7 RXD <- PA0-TX-UART4
# 12 3.3V
# 32 /RESET <- PA5-GPIO


import time
import sys
if not sys.platform == 'pyboard':
    import serial
    TTYADDR = "/dev/ttyAMA0"
else:
    import pyb


class RN2XX3():
    """Microchip RN2903 and RN2483 LoRa Wireless Modules

    This class implements all the functions that are available in the
    modules for evaluation.
    """

    COMMANDS = {
        "SYS_SLEEP":b"sys sleep {}",
        "SYS_RST":b"sys reset",
        "SYS_FACRST":b"sys factoryRESET",
        "SYS_ERASEFW":b"sys eraseFW",

        "SYS_VER":b"sys get ver",
        "SYS_VDD":b"sys get vdd",
        "SYS_HWEUI":b"sys get hweui",
        "SYS_NVMAT":b"sys get nvm {}",

        "SYS_NVMSET":b"sys set nvm {} {}",
        "SYS_PINCFG":b"sys set pindig {0} {1}",

        "MAC_RSTBAND":b"mac reset {}",
        "MAC_TX":b"mac tx {0} {1} {2}",
        "MAC_SAVE":b"mac save",
        "MAC_PAUSE":b"mac pause",
        "MAC_RESUME":b"mac resume",

        "MAC_DEVADDR":b"mac get devaddr",
        "MAC_DEVEUI":b"mac get deveui",
        "MAC_APPEUI":b"mac get appeui",
        "MAC_DR":b"mac get dr",
        "MAC_BAND":b"mac get band",
        "MAC_PWRIDX":b"mac get pwridx",
        "MAC_ADR":b"mac get adr",
        "MAC_RETX":b"mac get retx",
        "MAC_RXDELAY1":b"mac get rxdelay1",
        "MAC_RXDELAY2":b"mac get rxdelay2",
        "MAC_AR":b"mac get ar",
        "MAC_RX2":b"mac get rx2 {}",
        "MAC_DYCLEPS":b"mac get dcycleps",
        "MAC_MRGN":b"mac get mrgn",
        "MAC_GWNB":b"mac get gwnb",
        "MAC_STATUS":b"mac get status",

        "MAC_DEVADDRSET":b"mac set devaddr {}",
        "MAC_DEVEUISET":b"mac set deveui {}",
        "MAC_APPEUISET":b"mac set appeui {}",
        "MAC_NWKSKEYSET":b"mac set nwkskey {}",
        "MAC_APPSKEYSET":b"mac set appskey {}",
        "MAC_PWRIDXSET":b"mac set pwridx {}",
        "MAC_DRSET":b"mac set dr {}",
        "MAC_ADRSET":b"mac set adr {}",
        "MAC_BATSET":b"mac set bat {}",
        "MAC_RETXSET":b"mac set retx {}",
        "MAC_LINKCHKSET":b"mac set linkchk {}",
        "MAC_RXDELAY1SET":b"mac set rxdelay1 {}",
        "MAC_ARSET":b"mac set ar {}",
        "MAC_RXSET":b"mac set rx2 {0} {1}",

    }


    def __init__(self, ser=None, verbose=False):
        self.verbose = verbose
        self.ser = ser
        if self.ser == None:
            raise ValueError('No valid serial port')
        # execute reset of the module by pulling down a pin
        if sys.platform == "pyboard":
            RN_RESET_PIN = pyb.Pin(pyb.Pin.cpu.A5, mode=pyb.Pin.OUT_PP)
            RN_RESET_PIN.value(1)
            time.sleep(0.25)
            RN_RESET_PIN.value(0)
            time.sleep(0.25)
            RN_RESET_PIN.value(1)

    def getConn(self):
        return self.ser

    def closeConn(self):
        if not sys.platform == "pyboard":
            self.ser.close()
        else:
            self.ser.deinit()

    def execCmd(self, cmd):
        if self.verbose:
            print("Attempting to execute command: {}\r\n".format(cmd))
        self.ser.write(cmd)
        self.ser.write("\r\n")
        line = self.ser.readline()
        if self.verbose:
            print("Command response: {}\r\n".format(line))
        return line

    # SYS COMMANDS

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

    # MAC COMMANDS

    def getMacDeveui(self):
        return self.execCmd(self.COMMANDS["MAC_DEVEUI"])


def main():
    """ """
    if not sys.platform == "pyboard":
        # in this case a Raspi
        ser = serial.Serial(TTYADDR, 57600, timeout=5)
    else:
        ser = pyb.UART(4, baudrate=57600, timeout=5000)

    loraClient = RN2XX3(ser=ser, verbose=False)

    print("\r\nCHIP FIRMWARE VERSION IS: {}".format(loraClient.getSysVersion() ))
    time.sleep(1)
    print("\r\nCHIP HARDWARE EUI IS: {}".format(loraClient.getSysHweui() ))
    time.sleep(1)
    print("\r\nCHIP VDD READING IS: {}".format(loraClient.getSysVdd() ))
    time.sleep(1)
    print("\r\nCHIP MAC DEVEUI IS: {}".format(loraClient.getMacDeveui() ))
    print("SLEEPING WITH RN2XX3 CHIP\r\n {}".format(loraClient.sysSleep(3000) ))
    print("SETTING NVM AT 3FF TO 88: {}".format(loraClient.setSysNvmAg('3FF','88') ))
    time.sleep(0.25)
    print("\nNVM MEMORY VALUE AT: 3FF IS: {}".format(loraClient.getSysNvmAt('3FF')) )
    print("RESETTING CLIENT {}".format(loraClient.sysReset()))
    loraClient.closeConn()


if __name__ == "__main__":
    main()
