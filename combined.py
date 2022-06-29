import time
import csv
import sys
import os
import busio
import board
import schedule
import threading
import adafruit_mcp9808
from datetime import datetime
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

i2c = busio.I2C(board.SCL, board.SDA)
i2c_bus = board.I2C()
ina219A = INA219(i2c_bus, 0x40)
ina219B = INA219(i2c_bus, 0x44)
ina219C = INA219(i2c_bus, 0x45)
mcp = adafruit_mcp9808.MCP9808(i2c)


now = datetime.now()
timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
print(timestr)
datafile = open(timestr+".csv",'a',newline='')
csvWriter = csv.writer(datafile)
timeleft = 1800
while timeleft>0:
    i2c = busio.I2C(board.SCL, board.SDA)
    tempC = mcp.temperature
    tempF = tempC * 9 / 5 + 32
    bus_voltageA = ina219A.bus_voltage  # voltage on V- (load side)
    shunt_voltageA = ina219A.shunt_voltage  # voltage between V+ and V- across the shunt
    currentA = ina219A.current  # current in mA
    powerA = ina219A.power  # power in watts
    bus_voltageB = ina219B.bus_voltage  # voltage on V- (load side)
    shunt_voltageB = ina219B.shunt_voltage  # voltage between V+ and V- across the shunt
    currentB = ina219B.current  # current in mA
    powerB = ina219B.power  # power in watts
    bus_voltageC = ina219C.bus_voltage  # voltage on V- (load side)
    shunt_voltageC = ina219C.shunt_voltage  # voltage between V+ and V- across the shunt
    currentC = ina219C.current  # current in mA
    powerC = ina219C.power  # power in watts
    print("Temperature: {} C".format(tempC))##Robin- we don't need both temps, just temp C, easy to convert 
    print("Voltage A (VIN+) : {:6.3f}   V".format(bus_voltageA + shunt_voltageA))
    print("Voltage A (VIN-) : {:6.3f}   V".format(bus_voltageA))
    print("Power Calc. A    : {:8.5f} W".format(bus_voltageA * (currentA / 1000)))
    print("Power Register A : {:6.3f}   W".format(powerA))
    print("")
    print("Voltage B (VIN+) : {:6.3f}   V".format(bus_voltageB + shunt_voltageB))
    print("Voltage B (VIN-) : {:6.3f}   V".format(bus_voltageB))
    print("Power Calc. B    : {:8.5f} W".format(bus_voltageB * (currentB / 1000)))
    print("Power Register B : {:6.3f}   W".format(powerB))
    print("")
    print("Voltage C (VIN+) : {:6.3f}   V".format(bus_voltageC + shunt_voltageC))
    print("Voltage C (VIN-) : {:6.3f}   V".format(bus_voltageC))
    print("Power Calc. C    : {:8.5f} W".format(bus_voltageC * (currentC / 1000)))
    print("Power Register C : {:6.3f}   W".format(powerC))
    print("")
    csvWriter.writerow([tempC,"C"])
    csvWriter.writerow(['Voltage A (bus,shunt) :', bus_voltageA,'V', shunt_voltageA,'V', 'Power Calc. :',bus_voltageA * (currentA / 1000),'W', 'Power register :', powerA, 'W'])
    csvWriter.writerow(['Voltage B (bus,shunt) :', bus_voltageB,'V', shunt_voltageB,'V', 'Power Calc. :',bus_voltageB * (currentB / 1000),'W', 'Power register :', powerB, 'W'])
    csvWriter.writerow(['Voltage C (bus,shunt) :', bus_voltageC,'V', shunt_voltageC,'V', 'Power Calc. :',bus_voltageC * (currentC / 1000),'W', 'Power register :', powerC, 'W'])
    time.sleep(2)
    timeleft=timeleft-2
    while timeleft<=0:
        datafile = open(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".csv",'a',newline='')
        csvWriter = csv.writer(datafile)##Robin- Why are you changing the delimiter to tabs instead of comma's?
        i2c = busio.I2C(board.SCL, board.SDA)
        tempC = mcp.temperature
        tempF = tempC * 9 / 5 + 32
        bus_voltageA = ina219A.bus_voltage  # voltage on V- (load side)
        shunt_voltageA = ina219A.shunt_voltage  # voltage between V+ and V- across the shunt
        currentA = ina219A.current  # current in mA
        powerA = ina219A.power  # power in watts
        bus_voltageB = ina219B.bus_voltage  # voltage on V- (load side)
        shunt_voltageB = ina219B.shunt_voltage  # voltage between V+ and V- across the shunt
        currentB = ina219B.current  # current in mA
        powerB = ina219B.power  # power in watts
        bus_voltageC = ina219C.bus_voltage  # voltage on V- (load side)
        shunt_voltageC = ina219C.shunt_voltage  # voltage between V+ and V- across the shunt
        currentC = ina219C.current  # current in mA
        powerC = ina219C.power  # power in watts
        print("Temperature: {} C".format(tempC))##Robin- we don't need both temps, just temp C, easy to convert 
        print("Voltage A (VIN+) : {:6.3f}   V".format(bus_voltageA + shunt_voltageA))
        print("Voltage A (VIN-) : {:6.3f}   V".format(bus_voltageA))
        print("Power Calc. A    : {:8.5f} W".format(bus_voltageA * (currentA / 1000)))
        print("Power Register A : {:6.3f}   W".format(powerA))
        print("")
        print("Voltage B (VIN+) : {:6.3f}   V".format(bus_voltageB + shunt_voltageB))
        print("Voltage B (VIN-) : {:6.3f}   V".format(bus_voltageB))
        print("Power Calc. B    : {:8.5f} W".format(bus_voltageB * (currentB / 1000)))
        print("Power Register B : {:6.3f}   W".format(powerB))
        print("")
        print("Voltage C (VIN+) : {:6.3f}   V".format(bus_voltageC + shunt_voltageC))
        print("Voltage C (VIN-) : {:6.3f}   V".format(bus_voltageC))
        print("Power Calc. C    : {:8.5f} W".format(bus_voltageC * (currentC / 1000)))
        print("Power Register C : {:6.3f}   W".format(powerC))
        print("")
        csvWriter.writerow([tempC,"C"])
        csvWriter.writerow(['Voltage A (bus,shunt) :', bus_voltageA,'V', shunt_voltageA,'V', 'Power Calc. :',bus_voltageA * (currentA / 1000),'W', 'Power register :', powerA, 'W'])
        csvWriter.writerow(['Voltage B (bus,shunt) :', bus_voltageB,'V', shunt_voltageB,'V', 'Power Calc. :',bus_voltageB * (currentB / 1000),'W', 'Power register :', powerB, 'W'])
        csvWriter.writerow(['Voltage C (bus,shunt) :', bus_voltageC,'V', shunt_voltageC,'V', 'Power Calc. :',bus_voltageC * (currentC / 1000),'W', 'Power register :', powerC, 'W'])
        time.sleep(2)
        timeleft=timeleft+1800
