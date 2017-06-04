# python-lorawan-RN2XX3

http://ww1.microchip.com/downloads/en/DeviceDoc/40001811A.pdf

This is the start of a python wrapper around the serial command API for Microchip RN2483 and RN2903 LoRaWAN using Tindie breakout

This project uses a RN3903A, on a breakout purchased from Azzy's Electronics on Tindie, here:

https://www.tindie.com/stores/DrAzzy/
https://www.tindie.com/products/DrAzzy/lorawan-rn2483rn2903-breakout-board-assembled/

This breakout is directly powered and connected by a Raspberry Pi Zero with Wifi and Ble (not a ZeroW, but technically the same).  The wiring for this is show on the Tindie site above, or her:

http://drazzy.com/e/products/img/RN2483diagram2.jpg

UART must be enabled and the serial console must be turned off, on the RPi. I haven't configured RTS/CTS yet, on the RPi, but it doesn't seem to be needed so far.

https://www.dropbox.com/s/ht7ks8y3po88wfw/RN2903.jpg?dl=0 
