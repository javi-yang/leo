import usb.core
import usb.util

def read(device, endpoint_address, length):
        try:
            device.set_configuration()
            data = device.read(endpoint_address, length)
            print(f"got:{data}")
            return data

        except usb.core.USBError as e:
            print(e)
            return None
#device = usb.core.find(idVendor=0x046d, idProduct=0xc52f)
device = usb.core.find(idVendor=0x16d0, idProduct=0x117e)
print(device)
'''
for cfg in device:
    pass
    for intf in cfg:
        pass
    
        for ep in intf:
            print(f"E: {ep.bEndpointAddress:02x}")
'''
if device is None:
    print('none')
else:
    read(device, 0x81, 64)
#print(devices)
