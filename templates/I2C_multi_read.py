import smbus
import time

address = 0x6e

bus = smbus.SMBus(1)

count = 0x41


print("ADR:",hex(address),'\r\n')

while count < 0x48:

    data = bus.read_byte_data(address,count)
    print("Register:",hex(count),"    Value:",hex(data),'\r\n')
    
    count += 1

bus.close