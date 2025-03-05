# Implementation for a SUYEEGO SYG-MPPT-120A 500V 120A mppt solar charge controller

import time
import sys, os, io
import struct

# RS-232 custom protocol close to Modbus, but no sigar... 
import serial

sleepTime = 10

try:
    scc = serial.Serial('/dev/ttyUSB0')
    scc.baudrate = 2400 # The 80's called, they want their Baud Rate back.
    scc.timeout  = 0.2
except:
    print("HV SCC not found.")

# The hex string composing the command, including CRC check etc.
def sendSCCCommand(cmd_string):
    cmd_bytes = bytearray.fromhex(cmd_string)
    for cmd_byte in cmd_bytes:
        hex_byte = ("{0:02x}".format(cmd_byte))
        scc.write(bytearray.fromhex(hex_byte))
    return

# This could be much better, but it works.
def readSCC(fileObj):
    try: 
        # Read Battery, PV voltage
        sendSCCCommand('05 03 11 95 00 15 90 91')
        time.sleep(.5)
        if scc.inWaiting() >= 4 :
            if scc.read(1).hex() == '05' : # header byte 1
                if scc.read(1).hex() == '03' : # header byte 2
                    # Read all the data
                    available = scc.inWaiting()
                    data = bytearray(scc.read(available))
                    # length of data, without length byte or checksum
                    length = data[0]
 
                    # make sure we have all the data
                    if available - length != 3:
                        scc.reset_input_buffer()
                        raise Exception("Data incomplete.")

                    # PV Voltage
                    pvVolts = struct.unpack_from('<H', data, 7)[0]/10
                    valName  = "mode=\"pvVolts\""
                    valName  = "{" + valName + "}"
                    dataStr  = f"HV_SCC{valName} {pvVolts}"
                    print(dataStr, file=fileObj)
        
                    # Battery Voltage
                    batVolts = struct.unpack_from('<H', data, 11)[0]/10
                    valName  = "mode=\"batVolts\""
                    valName  = "{" + valName + "}"
                    dataStr  = f"HV_SCC{valName} {batVolts}"
                    print(dataStr, file=fileObj)

                    loadWatts = struct.unpack_from('<H', data, 9)[0]
                    valName  = "mode=\"loadWatts\""
                    valName  = "{" + valName + "}"
                    dataStr  = f"HV_SCC{valName} {loadWatts}"
                    print(dataStr, file=fileObj)
                    
        scc.reset_input_buffer()

    except Exception as e :
        print(e)



while True:
    file_object = open('/ramdisk/SCC_HV.prom.tmp', mode='w')
    readSCC(file_object)
    file_object.flush()
    file_object.close()
    outLine = os.system('/bin/mv /ramdisk/SCC_HV.prom.tmp /ramdisk/SCC_HV.prom')
    
    time.sleep(sleepTime)

