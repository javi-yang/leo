'''
ser.read(num)   
ser.inWaiting()    
'''
import serial
import struct
import time
import os
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyUSB1", 115200, timeout = 2)
ser.flushInput()

channel_1 = 11
channel_2 = 13
channel_3 = 15
channel_4 = 29
channel_list = [channel_1, channel_2, channel_3, channel_4]
'''
!!!CAUTION!!!  !!!PULL-UP/DOWN SETTING!!!
'''
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(channel_list,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel_1, GPIO.RISING, bouncetime = 1000)
GPIO.add_event_detect(channel_2, GPIO.RISING, bouncetime = 1000)
GPIO.add_event_detect(channel_3, GPIO.RISING, bouncetime = 1000)


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
    
def wait_msg():
    while True:
        
        time.sleep(5)
        count = ser.inWaiting()

        if count !=0:
            break


def lemans_login():
    print("AUTO LOGIN >>>")
    time.sleep(1)
    ser.write("root\r\n".encode())
    time.sleep(1)
    ser.write("oelinux123\r\n".encode())
    time.sleep(5)
'''
    ser.write("dmesg -n 1\r\n".encode())
    time.sleep(1)
    readback()
    ser.write("usb_device_mode.sh\r\n".encode())
    time.sleep(5)
    readback()
    time.sleep(15)
    print("15seconds----")
    time.sleep(15)
    print("continue----")   
    os.system('sudo adb root')
    time.sleep(2)
    os.system('sudo adb shell')
    time.sleep(2)
    os.system('./tunersoft')    
    time.sleep(5)
    readback()
'''
    ser.write("alsaucm -n -b - << EOM\r\n".encode())
    readback()
    ser.write("open sa8255-adp-star-snd-card\r\n".encode())
    readback()
    ser.write("set _verb Record2\r\n".encode())
    readback()
    ser.write("EOM\r\n".encode())
    time.sleep(2)
    readback()
    ser.write("arecord -Dagm:1,103 -f S16_LE -c 2 -r 48000 /tmp/new.wav &\r\n".encode())

    
def test_cmd():
    print("TEST_CMD >>>")
    readback()    
    ser.write("usb_device_mode.sh\r\n".encode())
    time.sleep(5)
    #readback()
    os.system('sudo adb root')
    time.sleep(2)
    os.system('sudo adb shell')
    time.sleep(2)
    os.system('./tunersoft')    
    time.sleep(5)
    readback()
    
    
    '''
    os.system('alsaucm -n -b - << EOM')
    time.sleep(2)
    os.system('open sa8255-adp-star-snd-card')
    time.sleep(2)
    os.system('set _verb Record2')
    time.sleep(2)
    os.system('EOM')
    time.sleep(2)
    readback()
    os.system('arecord -Dagm:1,103 -f S16_LE -c 2 -r 48000 /tmp/new.wav &')
    readback()
    '''
    ser.write("alsaucm -n -b - << EOM\r\n".encode())
    readback()
    ser.write("open sa8255-adp-star-snd-card\r\n".encode())
    readback()
    ser.write("set _verb Record2\r\n".encode())
    readback()
    ser.write("EOM\r\n".encode())
    time.sleep(2)
    readback()
    ser.write("arecord -Dagm:1,103 -f S16_LE -c 2 -r 48000 /tmp/new.wav &\r\n".encode())

        
def A2B_play():
    print("A2B PLAY START >>>")
    #ser.write("aplay_a2b2.sh &\r\n".encode())
    ser.write("usb_device_mode.sh\r\n".encode())
    time.sleep(5)
    readback()
    os.system('sudo adb root')
    time.sleep(2)
    os.system('sudo adb push /home/pi/reg_setting.sh /home/root')
    time.sleep(5)
    os.system('chmod +x reg_setting.sh')
    time.sleep(2)
    ser.write("aplay_a2b2.sh &\r\n".encode())
    time.sleep(10)
    readback()
    ser.write("./reg_setting.sh\r\n".encode())
    readback()
    time.sleep(10)
    #wait_msg()
    readback()
    ser.write("alsaucm -n -b - << EOM\r\n".encode())
    readback()
    ser.write("open sa8255-adp-star-snd-card\r\n".encode())
    readback()
    ser.write("set _verb HiFi\r\n".encode())
    readback()
    ser.write("EOM\r\n".encode())
    time.sleep(2)
    readback()
    ser.write("aplay -Dagm:1,0 /etc/acdb-blob/testaudio.wav\r\n".encode())
    

def A2B_record():
    print("A2B RECORD START >>>")
    #ser.write("usb_device_mode.sh\r\n".encode())
    time.sleep(1)
    ser.write("arecord_a2b2.sh /home/root/Test_a2b2.wav\r\n".encode())
    time.sleep(1)

def CAN_send():
    while True:
        ser.write("echo -e \"0,1,2,3,4,5,6,7,8,9,0,0,0,0,0,0\">/tmp/can_write.txt\r\n".encode())
        ser.write("CAN_Message_Send\r\n".encode())
        #ser.write("CAN_Reception\r\n".encode())
        time.sleep(3)
        readback()        
        if GPIO.event_detected(channel_3):
            print("***CAN cycle stop***")
            break

def I2C_dump():
    ser.write("i2cdump -y -f 7 0x69\r\n".encode())
    #ser.write("i2cdetect -a\r\n".encode())

def I2C_set():
    #ser.write("i2cset -y -f 7 0x68 0x12 0x03\r\n".encode())
    ser.write("i2cset -y -f 7 0x68 0x11 0x23\r\n".encode())
    #ser.write("i2cset -y -f 7 0x69 0x42 0x93\r\n".encode())
    #ser.write("i2cset -y -f 7 0x69 0x47 0x00\r\n".encode())    

def func_in():
    if GPIO.input(channel_4):                  # HKP-WDT-OFF DOWN
        if GPIO.event_detected(channel_1):
            #lemans_login()
            test_cmd()
        if GPIO.event_detected(channel_2):
            A2B_record()
        if GPIO.event_detected(channel_3):
            A2B_play()
    else:
        if GPIO.event_detected(channel_1):
            I2C_dump()
        if GPIO.event_detected(channel_2):
            I2C_set()
        if GPIO.event_detected(channel_3):
            CAN_send()

#ser.write("pkill -9 aplay\r\n".encode())
#time.sleep(2)


while True:

    func_in()
    
    count = ser.inWaiting()    
    if count != 0:
        data = ser.readline()
        data = data.strip()
        data = bytes.decode(data, errors="ignore")
        print(data)
       
        if data.find("lemans login:"):
            pass
        else:
            time.sleep(2)
            readback()
            lemans_login()
            time.sleep(2)
            #test_cmd()
            readback()

    time.sleep(0.01)
