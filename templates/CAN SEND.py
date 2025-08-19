import serial
import time
ser = serial.Serial("/dev/ttyUSB0", 115200)    # 第一个参数就是上面那个黄色字体  第二个参数填波特率
ser.flushInput()    # 清除缓存


while True:
    count = ser.inWaiting()
        
    if count != 0:
        data = ser.readline()
        data = data.strip()
        data = bytes.decode(data, errors="ignore")
        print(data)

    time.sleep(0.01)

