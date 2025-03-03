# SYG-MPPT-120A_grafana
Implementation for a SUYEEGO SYG-MPPT-120A 500V 120A mppt solar charge controller.
This script is intended to be used with:
https://github.com/BarkinSpider/SolarShed/

This charge controller can be found on Alibaba:
https://offer.alibaba.com/cps/f4jdbq3f?bm=cps&src=saf&productId=1601042916583

A 500V input capable MPPT controller for a price around US$140 - it's a bargain. 

The controller has two communication interfaces: a BMS port and a WIFI port. The BMS port is RS-485 and uses a protocol compatible with the PACE BMS.
The WIFI port uses RS-232, and is used to connect a Solar Plug (RWB1) RS232 To Wi-Fi+BLE Collector. This allows data from the device to be transmitted to a cloud platform called "Solar of Things"... So instead of doing that, this code hooks up to the port to read the data for graphing with Grafana. 

You will need a true RS-232 (not UART) converter, something like this: https://s.click.aliexpress.com/e/_oEWW42w
With a typical straight UTP/STP cable, pin one, two and three (orange/white, orange, green/white) correspond to RXD, GND and TXD respectively. 
