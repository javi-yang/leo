'''
ser.read(num)   
ser.inWaiting()    
'''
import serial
import struct
import time
import RPi.GPIO as GPIO
import datetime

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout = 2 )
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

ct = 0

def readback():
    while True:
        count = ser.inWaiting()
        
        if count != 0:

            data = ser.readline()
            data = data.strip()
            data = bytes.decode(data, errors="ignore")
            print(data)
            time.sleep(0.1)

        else:
            break
        time.sleep(0.01)

def lemans_login():
    print("AUTO LOGIN >>>")
    time.sleep(1)
    ser.write("root\r\n".encode())
    time.sleep(1)
    ser.write("oelinux123\r\n".encode())
    time.sleep(1)
        
def A2B_play():
    print("A2B PLAY START >>>")
    #ser.write("aplay_a2b2.sh &\r\n".encode())
    ser.write("aout_a2b2.sh &\r\n".encode())
    #time.sleep(10)
    readback()
'''
    ser.write("reg_set_a2b2.sh\r\n".encode())
    time.sleep(1)
    readback()
    ser.write("alsaucm -n -b - << EOM\r\n".encode())
    time.sleep(2)
    ser.write("open sa8255-adp-star-snd-card\r\n".encode())
    time.sleep(2)
    ser.write("set _verb HiFi\r\n".encode())
    time.sleep(2)
    ser.write("EOM\r\n".encode())
    time.sleep(2)
    ser.write("aplay -Dagm:1,0 /etc/acdb-blob/testaudio.wav\r\n".encode())
    time.sleep(1)
'''
    
def A2B_record():
    print("A2B RECORD START >>>")
    #ser.write("usb_device_mode.sh\r\n".encode())
    time.sleep(1)
    ser.write("arecord_a2b2.sh /home/root/Test_a2b2.wav\r\n".encode())
    time.sleep(1)

def CAN_send():
    while True:
        #ser.write("echo -e "0,1,2,3,4,5,6,7,8,9,0,0,0,0,0,0">/tmp/can_write.txt\r\n".encode())
        ser.write("CAN_Message_Send\r\n".encode())
        #ser.write("CAN_Reception\r\n".encode())
        time.sleep(3)
        readback()        
        if GPIO.event_detected(channel_3):
            print("***CAN cycle stop***")
            break
    
def func_in():
    if GPIO.input(channel_4):                  # HKP-WDT-OFF DOWN
        if GPIO.event_detected(channel_1):
            lemans_login()
        if GPIO.event_detected(channel_2):
            A2B_record()
        if GPIO.event_detected(channel_3):
            A2B_play()
    else:
        if GPIO.event_detected(channel_3):
            CAN_send()

#ser.write("pkill -9 aplay\r\n".encode())
#time.sleep(2)


while True:
    
    readback()
    
    ct += 1

    if(ct == 3):
        ser.write("888\r\n".encode())
        ct = 0
    time.sleep(2)
    readback()
    '''
    count = ser.inWaiting()    
    if count != 0:

        data = ser.readline()
        data = data.strip()
        data = bytes.decode(data, errors="ignore")

        print(data)
    '''
    time.sleep(2)
'''
    else:
        print('ERR!!!!!!!!!!!')
    
    time.sleep(2)
    count = 0
'''        
       
    
    #time.sleep(0.01)
