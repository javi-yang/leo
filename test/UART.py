'''
ser.read(num)   
ser.inWaiting()    
'''
import serial
import struct
import time
import os
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout = 2)
ser.flushInput()

ser_bt = serial.Serial("/dev/rfcomm0", 115200, timeout = 5)
ser_bt.flushInput()

data_bt = 1

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

GPIO.setup(7, GPIO.OUT)
#GPIO.output(7, 1)


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
    
def wait_msg():
    while True:
        
        time.sleep(5)
        count = ser.inWaiting()

        if count !=0:
            break

        


def lemans_login():
    print("AUTO LOGIN >>>")
    ser.write("root\r\n".encode())
    time.sleep(1)
    ser.write("oelinux123\r\n".encode())
    
def test_cmd():
    print("TEST_CMD >>>")
    #ser.write("usb_device_mode.sh\r\n".encode())
    ser.write("aout_a2b2.sh\r\n".encode())
        
def A2B_play():
    print("A2B PLAY START >>>")
    #ser.write("aout_a2b_Amp.sh\r\n".encode())
    ser.write("aout_a2b2.sh\r\n".encode())
    readback()
    time.sleep(2)
    readback()
    '''
    ser.write("i2cset -y -f 7 0x68 0x01 0x00\r\n".encode())
    ser.write("i2cset -y -f 7 0x69 0x00 0x10\r\n".encode())
    #time.sleep(1)
    ser.write("i2cset -y -f 7 0x69 0x07 0x92\r\n".encode())
    #time.sleep(1)
    ser.write("i2cset -y -f 7 0x68 0x01 0x00\r\n".encode())
    ser.write("i2cset -y -f 7 0x69 0x00 0x11\r\n".encode())
    #time.sleep(1)
    ser.write("i2cset -y -f 7 0x69 0x07 0x92\r\n".encode())
    
    
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
    
def func_002():
    ser.write("i2cget -y -f 7 0x68 0x17\r\n".encode())

def I2C_set():

    ser.write("i2cset -y -f 7 0x68 0x11 0x23\r\n".encode())

def terminal():
    '''
    os.system('i2cdump -y -f 1 0x10')
    time.sleep(1)
    os.system('i2cdump -y -f 1 0x11')
    time.sleep(1)
    '''
    os.system('i2cset -y -f 1 0x10 0x07 0x92')
    time.sleep(0.3)
    os.system('i2cset -y -f 1 0x11 0x07 0x92')
    '''
    c
    ser.write("i2cset -y -f 7 0x69 0x00 0x10\r\n".encode())
    #time.sleep(1)
    ser.write("i2cset -y -f 7 0x69 0x07 0x92\r\n".encode())
    #time.sleep(1)
    ser.write("i2cset -y -f 7 0x68 0x01 0x00\r\n".encode())
    ser.write("i2cset -y -f 7 0x69 0x00 0x11\r\n".encode())
    #time.sleep(1)
    ser.write("i2cset -y -f 7 0x69 0x07 0x92\r\n".encode())
    '''
def func_004():

    time.sleep(0.5)
    ser.write("i2cget -y -f 7 0x68 0x17\r\n".encode())
        
        
def func_list():
    ser_bt.write("\r\n".encode())
    ser_bt.write("A: A2B play\r\n".encode())
    ser_bt.write("B: TERMINAL\r\n".encode())
    ser_bt.write("C: A2B record\r\n".encode())
    ser_bt.write("D: I2C DETECT\r\n".encode())
    ser_bt.write("P: I2C DUMP\r\n".encode())
    ser_bt.write("R: reboot\r\n".encode())
    ser_bt.write("U: USB device mode\r\n".encode())
    ser_bt.write("001: TEST\r\n".encode())
    ser_bt.write("002: I2C GET MANUAL -> DEVICE ADR\r\n".encode())
    ser_bt.write("003: I2C GET AUTO 0x68 0x17\r\n".encode())
    ser_bt.write("004: I2C GET cycle 0x68 0x17\r\n".encode())
    ser_bt.write("005: GPIO_7 output\r\n".encode())
    ser_bt.write("006: GPIO_7 interrupt\r\n".encode())
    ser_bt.write("011: aout AMP T01_MENUETTO\r\n".encode())
    ser_bt.write("012: aout ADZS T01_MENUETTO\r\n".encode())
    ser_bt.write("\r\n".encode())
    
    
    
'''    
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
'''

def bt_trans():
    count_bt = ser_bt.inWaiting()
    
    global data_bt
    
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
                time.sleep(0.1)
            if ('B' in data_bt):
                
                terminal()
            if ('C' in data_bt):
                A2B_record()
            if ('R' in data_bt):
                time.sleep(1)
                reboot()
            if ('D' in data_bt):
                time.sleep(0.1)
                ser.write("i2cdetect -y -r 7\r\n".encode())
            if ('P' in data_bt):
                time.sleep(0.1)
                I2C_dump()
            if ('U' in data_bt):
                time.sleep(0.1)
                ser.write("usb_device_mode.sh\r\n".encode())           
            if ('Z' in data_bt):
                time.sleep(0.1)
                func_list()

        elif ("001" in data_bt[:2]):
            print(data_bt[3:])
        elif (data_bt[:3] == '001'):
            #if ("01" in data_bt[1:2]):
            print(data_bt[3:])
        elif (data_bt[:3] == '002'):
            ser.write("i2cget -y -f 7 0x".encode())
            ser.write(data_bt[3:5].encode())
            ser.write(" 0x".encode())
            ser.write(data_bt[5:7].encode())
            ser.write("\r\n".encode())
        elif (data_bt[:3] == '003'):
            ser.write("i2cget -y -f 7 0x68 0x0d\r\n".encode())
            ser.write("i2cget -y -f 7 0x68 0x65\r\n".encode())
            ser.write("i2cget -y -f 7 0x68 0x66\r\n".encode())
            ser.write("i2cget -y -f 7 0x68 0x67\r\n".encode())
            ser.write("i2cget -y -f 7 0x68 0x68\r\n".encode())
        elif (data_bt[:3] == '004'):
            pass
        elif (data_bt[:3] == '005'):
            if (data_bt[3:4] == '1'): 
                GPIO.output(7, 1)
            if (data_bt[3:4] == '0'):
                GPIO.output(7, 0)
        elif (data_bt[:3] == '006'):
            GPIO.output(7, 1)
            time.sleep(0.1)
            GPIO.output(7, 0)
        elif (data_bt[:3] == '011'):
            ser.write("aout_a2b_Amp.sh T01_MENUETTO.wav\r\n".encode())
        elif (data_bt[:3] == '012'):
            ser.write("aout_a2b2.sh T01_MENUETTO.wav\r\n".encode())
            
        elif (data_bt[:3] == '999'):
            GPIO.cleanup
        else:
            if ("os" in data_bt[:2]):
                os.system(data_bt[3:])
                #print(data_bt[2:5])

            else:
                ser.write(data_bt.encode())
                ser.write("\r\n".encode())
                
        count_bt = 0

while True:

    #func_in()
    
    bt_trans()
    
    count = ser.inWaiting()
    
    if (data_bt == '004'):
        
        func_004()

    
    if count != 0:
        data = ser.readline()
        data = data.strip()
        data = bytes.decode(data, errors="ignore")
        print(data)
        if ('i2c_geni' in data):
            continue
        ser_bt.write("\n".encode())
        ser_bt.write(data.encode())
        if data.find("lemans login:"):
            pass
        else:
            readback()
            lemans_login()



    time.sleep(0.01)
