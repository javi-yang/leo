'''
ser.read(num)   
ser.inWaiting()    
'''
import serial
import struct
import time
import os
import threading
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout = 2)
ser.flushInput()

ser_bt = serial.Serial("/dev/rfcomm0", 115200, timeout = 2)
ser_bt.flushInput()

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
            ser_bt.write("\n".encode())
            ser_bt.write(data.encode())
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
    
def test_cmd():
    print("TEST_CMD >>>")
    #ser.write("usb_device_mode.sh\r\n".encode())
    ser.write("aout_a2b2.sh\r\n".encode())
        
def A2B_play():
    print("A2B PLAY START >>>")
    ser.write("aout_a2b2.sh &\r\n".encode())
    '''
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
    '''

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

def reboot():
    ser.write("reboot\r\n".encode())

def I2C_dump():
    ser.write("i2cdump -y -f 7 0x68\r\n".encode())
    time.sleep(0.2)
    readback()
    ser.write("i2cdump -y -f 7 0x69\r\n".encode())
    #ser.write("i2cdetect -a\r\n".encode())

def I2C_set():

    ser.write("i2cset -y -f 7 0x68 0x11 0x23\r\n".encode())

def terminal():
    os.system('i2cdump -y -f 1 0x6e')
    time.sleep(1)
    os.system('i2cdump -y -f 1 0x6f')
    time.sleep(1)
    
  

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


def bt_trans():
    global echo_bt
    while True:
        count_bt = ser_bt.inWaiting()
       
        if count_bt != 0:
            data_bt = ser_bt.readline()
            data_bt = data_bt.strip()
            data_bt = bytes.decode(data_bt, errors="ignore")
            time.sleep(0.1)
            print(">> BT RECEIVED: ", data_bt)
            time.sleep(0.1)
        
            cmd_len = len(data_bt)

            if cmd_len == 1:
                if ('A' in data_bt):
                    time.sleep(0.1)
                    A2B_play()
                    #ser_bt.write("re\r\n".encode())
                    time.sleep(0.1)
                if ('B' in data_bt):
                
                    terminal()
                if ('R' in data_bt):
                    time.sleep(1)
                    reboot()
                    #ser_bt.write("re\r\n".encode())
                    #time.sleep(1)
                if ('D' in data_bt):
                    time.sleep(0.1)
                    ser.write("i2cdetect -y -r 7\r\n".encode())
                if ('P' in data_bt):
                    time.sleep(0.1)
                    I2C_dump()
            
                if ('Z' in data_bt):
                    time.sleep(0.1)
                    
                    echo_bt = 1
                           
                           
                    #print(echo_bt)`
                    '''
                    ser_bt.write("\r\n".encode())
                    ser_bt.write("A: A2B play\r\n".encode())
                    ser_bt.write("B: TERMINAL\r\n".encode())
                    ser_bt.write("D: I2C DETECT\r\n".encode())
                    ser_bt.write("P: I2C DUMP\r\n".encode())
                    ser_bt.write("R: reboot\r\n".encode())
                    ser_bt.write("\r\n".encode())
                    '''
            else: 
                ser.write(data_bt.encode())
                ser.write("\r\n".encode())
                
            count_bt = 0


#ser.write("pkill -9 aplay\r\n".encode())
#time.sleep(2)

def actions():
    global echo_bt
    echo_bt = 0
    while True:

        func_in()
        
        count = ser.inWaiting()    
        if count != 0:
            data = ser.readline()
            data = data.strip()
            data = bytes.decode(data, errors="ignore")
            print(data)
            ser_bt.write("\n".encode())
            ser_bt.write(data.encode())
            if data.find("lemans login:"):
                pass
            else:
                time.sleep(2)
                readback()
                lemans_login()
                time.sleep(5)
                #test_cmd()

        
        if echo_bt != 0:
            
            ser_bt.write("cmdlist\r\n".encode())
            
            echo_bt = 0
            



    time.sleep(0.01)
    
ACTS = threading.Thread(target=actions)
BT_CMD = threading.Thread(target=bt_trans)
ACTS.start()
BT_CMD.start()
