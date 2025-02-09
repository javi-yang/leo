'''
ser.read(num)   
ser.inWaiting()    
'''
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import serial
import struct
import time
import os
import RPi.GPIO as GPIO
from datetime import datetime

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=2)
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
GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel_1, GPIO.RISING, bouncetime=1000)
GPIO.add_event_detect(channel_2, GPIO.RISING, bouncetime=1000)
GPIO.add_event_detect(channel_3, GPIO.RISING, bouncetime=1000)

GPIO.setup(7, GPIO.OUT)
# GPIO.output(7, 1)

def readback():
    while True:
        count = ser.inWaiting()
        
        if count != 0:
            data = ser.readline()
            data = data.strip()
            data = bytes.decode(data, errors="ignore")
            print(data)
            if 'leamans login:' in data:
                lemans_login()
            display_message(data)
        else:
            break
        time.sleep(0.01)

def wait_msg():
    while True:
        time.sleep(5)
        count = ser.inWaiting()

        if count != 0:
            break

def lemans_login():
    print("AUTO LOGIN >>>")
    ser.write("root\r\n".encode())
    time.sleep(1)
    ser.write("oelinux123\r\n".encode())

def test_cmd():
    print("TEST_CMD >>>")
    # ser.write("usb_device_mode.sh\r\n".encode())
    ser.write("aout_a2b2.sh\r\n".encode())

def A2B_play():
    print("A2B PLAY START >>>")
    # ser.write("aout_a2b_Amp.sh\r\n".encode())
    ser.write("aout_a2b2.sh\r\n".encode())
    readback()
    time.sleep(2)
    readback()

def A2B_record():
    print("A2B RECORD START >>>")
    ser.write("arecord_a2b2.sh /home/root/Test_a2b2.wav\r\n".encode())
    time.sleep(1)

def CAN_send():
    while True:
        ser.write("echo -e \"0,1,2,3,4,5,6,7,8,9,0,0,0,0,0,0\">/tmp/can_write.txt\r\n".encode())
        ser.write("CAN_Message_Send\r\n".encode())
        # ser.write("CAN_Reception\r\n".encode())
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
    # ser.write("i2cdetect -a\r\n".encode())

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

def func_004():
    time.sleep(0.5)
    ser.write("i2cget -y -f 7 0x68 0x17\r\n".encode())

'''
def log_trans():
    if ser_bt:
        with open('/home/javi/leo_share/log.txt', 'r') as f:
            for line in f.readlines():
                ser_bt.write(line.encode())
'''


def on_button1_click():
    test_cmd()

def on_button2_click():
    A2B_play()

def on_button3_click():
    lemans_login()

def on_button4_click():
    A2B_record()

def on_switch_toggle():
    if switch_var.get():
        GPIO.output(7, 1)
    else:
        GPIO.output(7, 0)

last_messages = []
current_message_index = -1

def on_enter_click(event=None):
    global last_messages, current_message_index
    data = entry.get()
    ser.write(data.encode() + "\r\n".encode())
    last_messages.append(data)
    if len(last_messages) > 10:
        last_messages.pop(0)
    current_message_index = -1
    entry.delete(0, tk.END)

def on_page_up(event=None):
    global current_message_index
    if last_messages:
        current_message_index = (current_message_index - 1) % len(last_messages)
        entry.delete(0, tk.END)
        entry.insert(0, last_messages[current_message_index])

def display_message(message):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)
    # Limit the number of lines to 500
    lines = text_area.get("1.0", tk.END).split("\n")
    if len(lines) > 500:
        text_area.delete("1.0", "2.0")

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("UART Control")
    root.geometry("1000x700")  # Set default window size

    # Create buttons
    button1 = tk.Button(root, text="Test Command", command=on_button1_click)
    button1.place(x=10, y=10, width=120, height=30)

    button2 = tk.Button(root, text="A2B Play", command=on_button2_click)
    button2.place(x=10, y=50, width=120, height=30)

    button3 = tk.Button(root, text="Lemans Login", command=on_button3_click)
    button3.place(x=10, y=90, width=120, height=30)

    button4 = tk.Button(root, text="A2B Record", command=on_button4_click)
    button4.place(x=10, y=130, width=120, height=30)

    # Create switch
    global switch_var
    switch_var = tk.IntVar()
    switch = tk.Checkbutton(root, text="GPIO7 Control", variable=switch_var, command=on_switch_toggle)
    switch.place(x=150, y=10, width=120, height=30)

    # Create input field and ENTER button
    global entry
    entry = tk.Entry(root)
    entry.place(x=150, y=50, width=300, height=30)
    entry.bind("<Return>", on_enter_click)
    entry.bind("<Up>", on_page_up)  # Bind Page Up key to on_page_up function
    
    enter_button = tk.Button(root, text="ENTER", command=on_enter_click)
    enter_button.place(x=150, y=90, width=120, height=30)

    # Create text area for displaying messages
    global text_area
    text_area = ScrolledText(root, height=15, width=113, state=tk.DISABLED)
    text_area.place(x=25, y=400, width=950, height=300)

    # Run the GUI event loop
    root.mainloop()

# Run the GUI in a separate thread
gui_thread = threading.Thread(target=create_gui)
gui_thread.daemon = True
gui_thread.start()

while True:

    #count = ser.inWaiting()

    readback()
    time.sleep(0.01)
'''
    if data_bt == '004':
        func_004()
    
    if count != 0:
        data = ser.readline()
        data = data.strip()
        data is bytes.decode(data, errors="ignore")
        print(data)
        if 'i2c_geni' in data:
            continue
        ser_bt.write("\n".encode())
        ser_bt.write(data.encode())
        if data.find("lemans login:"):
            pass
        else:
            readback()
            lemans_login()
'''



