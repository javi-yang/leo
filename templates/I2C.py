import smbus
import time

#address = 0x6e

bus = smbus.SMBus(1)

#num = [0x01, 0x97, 0x98]


bus.write_byte_data(0x6e, 0x41, 0xe0)
bus.write_byte_data(0x6e, 0x42, 0x93)
bus.write_byte_data(0x6e, 0x47, 0x00)

'''
bus.write_byte_data(0x6e, 0x0c, 0x00)
bus.write_byte_data(0x6e, 0x0d, 0x02)
bus.write_byte_data(0x6e, 0x0e, 0x00)
bus.write_byte_data(0x6e, 0x0f, 0x88)



bus.write_byte_data(0x6e, 0x65, 0x0f)
bus.write_byte_data(0x6e, 0x42, 0x03)
bus.write_byte_data(0x6e, 0x43, 0x00)

bus.write_byte_data(0x6e, 0x1b, 0x10)

bus.write_byte_data(0x6e, 0x4d, 0x80)



print("ADR:",hex(address),'\r\n')

for index, value in enumerate(num):
    register = num
    print("reigster: {register}")
    
    data = bus.read_byte_data(address,num)
    
    data = hex(data)
    
    print("value: {data}")
'''

bus.close