# SYG-MPPT-120A_grafana
Implementation for a SUYEEGO SYG-MPPT-120A 500V 120A mppt solar charge controller.
This script is intended to be used with:
https://github.com/BarkinSpider/SolarShed/

This charge controller can be found on Alibaba: 
https://offer.alibaba.com/cps/f4jdbq3f?bm=cps&src=saf&productId=1601042916583

For a 500V input capable MPPT controller for a price around US$140 it's a bargain. 

The controller has two communication interfaces: a BMS port and a WIFI port. The BMS port uses a protocol compatible with the PACE BMS.
The WIFI port uses RS-232, and is used to connect a Solar Plug (RWB1) RS232 To Wi-Fi+BLE Collector. This allows data from the device to be transmitted to 
