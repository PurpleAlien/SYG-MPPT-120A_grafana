# Implementation for a SUYEEGO SYG-MPPT-120A 500V 120A mppt solar charge controller

# RS-232 Modbus
import minimalmodbus
import time
import sys, os, io
import struct

sleepTime = 10

def swap_bytes(value):
    return struct.unpack('<H', struct.pack('>H', value))[0]

try: 
    scc = minimalmodbus.Instrument('/dev/ttyUSB0', 5, debug=False) # port name, slave address (in decimal)
    scc.serial.baudrate = 2400 # The 80's called, they want their Baud Rate back.
    scc.serial.timeout  = 0.5
except:
    print("HV SCC not found.")

# This could be much better, but it works.
def readSCC(fileObj):
    try:
        #'05 03 11 95 00 15 90 91' --> read from 4501 (decimal) 21 bytes funciton code 3 
        registers = scc.read_registers(4501, number_of_registers=21)

        # For some reason minimalmodbus swapping bytes doesn't work...
        registers = list(map(lambda x: swap_bytes(x),registers)) 

        # PV Voltage
        pvVolts = registers[3]/10
        valName  = "mode=\"pvVolts\""
        valName  = "{" + valName + "}"
        dataStr  = f"HV_SCC{valName} {pvVolts}"
        print(dataStr, file=fileObj)
        
        # Battery Voltage
        batVolts = registers[5]/10
        valName  = "mode=\"batVolts\""
        valName  = "{" + valName + "}"
        dataStr  = f"HV_SCC{valName} {batVolts}"
        print(dataStr, file=fileObj)

        # Battery Current
        batAmps = registers[7]
        valName  = "mode=\"batAmps\""
        valName  = "{" + valName + "}"
        dataStr  = f"HV_SCC{valName} {batAmps}" 
        print(dataStr, file=fileObj)       
           
        # PV Watts generated
        loadWatts = registers[4]
        valName  = "mode=\"loadWatts\""
        valName  = "{" + valName + "}"
        dataStr  = f"HV_SCC{valName} {loadWatts}"
        print(dataStr, file=fileObj)
        

    except Exception as e :
        print(e)

while True:
    file_object = open('/ramdisk/SCC_HV.prom.tmp', mode='w')
    readSCC(file_object)
    file_object.flush()
    file_object.close()
    outLine = os.system('/bin/mv /ramdisk/SCC_HV.prom.tmp /ramdisk/SCC_HV.prom')

    time.sleep(sleepTime)
