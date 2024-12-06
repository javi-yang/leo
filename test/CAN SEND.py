import serial
import time
ser = serial.Serial("/dev/ttyUSB0", 38400)    # 第一个参数就是上面那个黄色字体  第二个参数填波特率
ser.flushInput()    # 清除缓存

def readback():
    while True:
        count = ser.inWaiting()
        
        if count != 0:
            data = ser.readline()
            data = data.strip()
            data = bytes.decode(data, errors="ignore")
            print(data)
        else:
            break
        time.sleep(0.01)
'''
ser.write("root\r\n".encode())
time.sleep(5)
ser.write("oelinux123\r\n".encode())
time.sleep(10)
ser.write("CAN_Message_Send\r\n".encode())
'''
ser.write("AT".encode())
time.sleep(1)
ser.write("\r\n".encode())
readback()
time.sleep(1)
ser.write("NAME=JAVI".encode())
time.sleep(1)
ser.write("\r\n".encode())
readback()