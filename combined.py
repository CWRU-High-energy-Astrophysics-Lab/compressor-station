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
ina219 = INA219(i2c_bus)
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
    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = ina219.current  # current in mA
    power = ina219.power  # power in watts
    print("Temperature: {} C".format(tempC))##Robin- we don't need both temps, just temp C, easy to convert 
    print("Voltage (VIN+) : {:6.3f}   V".format(bus_voltage + shunt_voltage))
    print("Voltage (VIN-) : {:6.3f}   V".format(bus_voltage))
    print("Power Calc.    : {:8.5f} W".format(bus_voltage * (current / 1000)))
    print("Power Register : {:6.3f}   W".format(power))
    print("")
    csvWriter.writerow([tempC,"C", "Power Calc.:",bus_voltage * (current / 1000),"W", "Power register:",power, "W"])
    time.sleep(2)
    timeleft=timeleft-2
    while timeleft<=0:
        datafile = open(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".csv",'a',newline='')
        csvWriter = csv.writer(datafile)##Robin- Why are you changing the delimiter to tabs instead of comma's?
        i2c = busio.I2C(board.SCL, board.SDA)
        tempC = mcp.temperature
        tempF = tempC * 9 / 5 + 32
        bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
        shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
        current = ina219.current  # current in mA
        power = ina219.power  # power in watts
        print("Temperature: {} C {} F ".format(tempC, tempF))##Robin- we don't need both temps, just temp C, easy to convert 
        print("Voltage (VIN+) : {:6.3f}   V".format(bus_voltage + shunt_voltage))
        print("Voltage (VIN-) : {:6.3f}   V".format(bus_voltage))
        print("Power Calc.    : {:8.5f} W".format(bus_voltage * (current / 1000)))
        print("Power Register : {:6.3f}   W".format(power))
        print("")
        csvWriter.writerow([tempC,"C", "Power Calc.:",bus_voltage * (current / 1000),"W", "Power register:",power, "W"])
        time.sleep(2)
        timeleft=timeleft+1800