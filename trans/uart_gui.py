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

filter1_active = False
filter1_text = ""
filter2_active = False
filter2_text = ""

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

def toggle_button_power():
    if button_power.config('bg')[-1] == 'orange':
        button_power.config(bg="gray", activebackground="gray")
        GPIO.output(7, 1)
    else:
        button_power.config(bg="orange", activebackground="orange")
        GPIO.output(7, 0)

def toggle_filter1():
    global filter1_active, filter1_button, filter1_text
    if filter1_button.config('bg')[-1] == 'orange':
        filter1_button.config(bg="gray", activebackground="gray")
        filter1_active = False
    else:
        filter1_button.config(bg="orange", activebackground="orange")
        filter1_active = True
        filter1_text = filter1_entry.get()

def toggle_filter2():
    global filter2_active, filter2_button, filter2_text
    if filter2_button.config('bg')[-1] == 'orange':
        filter2_button.config(bg="gray", activebackground="gray")
        filter2_active = False
    else:
        filter2_button.config(bg="orange", activebackground="orange")
        filter2_active = True
        filter2_text = filter2_entry.get()

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
    global filter1_active, filter1_text, filter2_active, filter2_text
    if filter1_active and filter1_text in message:
        return
    if filter2_active and filter2_text not in message:
        return
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
    root.geometry("1200x900")  # Set default window size

    # Create buttons
    button1 = tk.Button(root, text="REBOOT", command=reboot)
    button1.place(x=10, y=10, width=200, height=50)

    button2 = tk.Button(root, text="Lemans Login", command=lemans_login)
    button2.place(x=10, y=70, width=200, height=50)

    button3 = tk.Button(root, text="A2B Play", command=A2B_play)
    button3.place(x=10, y=130, width=200, height=50)

    button4 = tk.Button(root, text="A2B Record", command=A2B_record)
    button4.place(x=10, y=190, width=200, height=50)

    button5 = tk.Button(root, text="A2B Record", command=A2B_record)
    button5.place(x=10, y=250, width=200, height=50)

    button6 = tk.Button(root, text="A2B Record", command=A2B_record)
    button6.place(x=10, y=310, width=200, height=50)

    button7 = tk.Button(root, text="Lemans Login", command=lemans_login)
    button7.place(x=220, y=70, width=200, height=50)

    button8 = tk.Button(root, text="A2B Play", command=A2B_play)
    button8.place(x=220, y=130, width=200, height=50)

    button9 = tk.Button(root, text="A2B Record", command=A2B_record)
    button9.place(x=220, y=190, width=200, height=50)

    button10 = tk.Button(root, text="A2B Record", command=A2B_record)
    button10.place(x=220, y=250, width=200, height=50)

    button11 = tk.Button(root, text="A2B Record", command=A2B_record)
    button11.place(x=220, y=310, width=200, height=50)

    # Create toggle button
    global button_power
    button_power = tk.Button(root, text="POWER", command=toggle_button_power, bg="gray", activebackground="gray")
    button_power.place(x=220, y=10, width=200, height=50)

    # Create input field and ENTER button
    global entry
    entry = tk.Entry(root)
    entry.place(x=10, y=370, width=600, height=30)
    entry.bind("<Return>", on_enter_click)
    entry.bind("<Up>", on_page_up)  # Bind Page Up key to on_page_up function
    
    enter_button = tk.Button(root, text="ENTER", command=on_enter_click)
    enter_button.place(x=620, y=370, width=120, height=30)

    # Create filter1 input field and button
    global filter1_entry, filter1_button
    filter1_entry = tk.Entry(root)
    filter1_entry.place(x=10, y=410, width=600, height=30)
    
    filter1_button = tk.Button(root, text="FILTER1", command=toggle_filter1, bg="gray", activebackground="gray")
    filter1_button.place(x=620, y=410, width=120, height=30)

    # Create filter2 input field and button
    global filter2_entry, filter2_button
    filter2_entry = tk.Entry(root)
    filter2_entry.place(x=10, y=450, width=600, height=30)
    
    filter2_button = tk.Button(root, text="FILTER2", command=toggle_filter2, bg="gray", activebackground="gray")
    filter2_button.place(x=620, y=450, width=120, height=30)

    # Create text area for displaying messages
    global text_area
    text_area = ScrolledText(root, height=15, width=113, state=tk.DISABLED)
    text_area.place(x=25, y=500, width=1150, height=350)

    # Run the GUI event loop
    root.mainloop()

# Run the GUI in a separate thread
gui_thread = threading.Thread(target=create_gui)
gui_thread.daemon = True
gui_thread.start()

while True:
    readback()
    time.sleep(0.01)



