# python-lorawan-RN2XX3

http://ww1.microchip.com/downloads/en/DeviceDoc/40001811A.pdf

This is the start of a python wrapper around the serial command API for Microchip RN2483 and RN2903 LoRaWAN using Tindie breakout.

This project uses a RN2903A, on a breakout purchased from Azzy's Electronics on Tindie.

[Azzys Electronics](http://drazzy.com/e/)

[Azzys Electronics on Tindie](https://www.tindie.com/stores/DrAzzy/)

[Assembled breakout w RN2903 or RN2483](https://www.tindie.com/products/DrAzzy/lorawan-rn2483rn2903-breakout-board-assembled/)

This breakout is directly powered and connected by a Raspberry Pi Zero with Wifi and Ble (not a ZeroW, but technically the same).  The wiring for this is shown on the Tindie site above, where you can buy the breakouts, or below for convenience.

The setup, used is the top one pictured below:
![Wiring Diagram](http://drazzy.com/e/products/img/RN2483diagram2.jpg)


On the RPi, UART must be enabled and the serial console must be turned off. 

I haven't configured RTS/CTS yet, on the RPi, but it doesn't seem to be needed so far.

Here's the setup, using AdaFruit T Cobbler, RPi Zero and breakout:

![RPI Zero and RN3903 over UART](https://github.com/miguellan/python-lorawan-RN2XX3/blob/master/RN2903.jpg?raw=true)

The goal of this project, is to create a simple library, and starting point, for anyone evaluating RN2XX3 LoRaWAN chips.  If you found this repo helpful, and want to contribute.  Please fork, and create a pull request with your changes, and it will be merged.

# micropython
Added some basic code to support micropython. The connections made:

RN2483 | LABEL | HOST 
 --- | --- | ---
1 | GND
2 | RTS | not connected
3 | CTS | not connected
6 | TXD | PA1-RX-UART4
7 | RXD | PA0-TX-UART4
12| 3.3V|
32|/RESET| PA5-GPIO

Session output:
```
>>> execfile("RN2903lib.py")
CHIP FIRMWARE VERSION IS: b'RN2483 0.9.5 Mar 24 2015 14:15:33\r\n'
CHIP HARDWARE EUI IS: b'RN2483 0.9.5 Mar 24 2015 14:15:33\r\n'
CHIP VDD READING IS: b'0004A30B001A7F98\r\n'
CHIP MAC DEVEUI IS: b'3243\r\n'
SLEEPING WITH RN2XX3 CHIP b'0004A30B001A7F98\r\n'
SETTING NVM AT 3FF TO 88: b'ok\r\n'
NVM MEMORY VALUE AT: 3FF IS: b'88\r\n'
RESETTING CLIENT b'RN2483 0.9.5 Mar 24 2015 14:15:33\r\n'
```
