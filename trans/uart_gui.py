'''
with Raspberry Pi 4B   
    
'''
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import serial
import struct
import time
import os
import RPi.GPIO as GPIO
from datetime import datetime
from queue import Queue

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

interval_time = 0.3

# Create a queue to buffer incoming data
data_queue = Queue()

def readback():
    while True:
        count = ser.inWaiting()
        
        if count != 0:
            data = ser.readline()
            data = data.strip()
            data = bytes.decode(data, errors="ignore")
            data_queue.put(data)
            if 'lemans login:' in data:
                lemans_login()
        else:
            break

def process_queue():
    while not data_queue.empty():
        data = data_queue.get()
        display_message(data)
        if button_reserve.config('bg')[-1] == 'orange':
            with open('/home/javi/leo_share/log.txt', 'a') as log_file:
                log_file.write(data + '\n')
    root.after(100, process_queue)  # Schedule the next queue processing

def default_message():
    global bt_address, wifi_address, eth_address
    with open('/home/javi/leo_share/default_message.txt', 'a') as default_message_file:
       for line in default_message_file.readlines():
            if "BT" in line:
                bt_address = line.split("BT:")[1]
            elif "WIFI" in line:
                wifi_address = line.split("WIFI:")[1]
            elif "ETH" in line:
                eth_address = line.split("ETH:")[1] 

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
    ser.write("aout_a2b2.sh T01_MENUETTO.wav\r\n".encode())

def A2B2_play():
    print("A2B2 PLAY START >>>")
    # ser.write("aout_a2b_Amp.sh\r\n".encode())
    ser.write("Play_A2B2\r\n".encode())
    
def A2B_AMP_play():
    print("A2B PLAY START >>>")
    # ser.write("aout_a2b_Amp.sh\r\n".encode())
    ser.write("aout_a2b_Amp.sh T01_MENUETTO.wav\r\n".encode())

    
def A2B_USB_play():
    print("A2B PLAY START >>>")
    # ser.write("aout_a2b_Amp.sh\r\n".encode())
    ser.write("aout_USB.sh testaudio.wav\r\n".encode())

def A2B_record():
    print("A2B RECORD START >>>")
    ser.write("arecord_a2b2.sh /home/root/Test_a2b2.wav\r\n".encode())
    
def STOP_aout():
    print("A2B STOP >>>")
    ser.write("stop_a2b.sh\r\n".encode())
    
def amp_record():
    #ser.write("aout_a2b_Amp.sh T01_MENUETTO.wav\r\n".encode())
    #time.sleep(2)
    ser.write("reg_a2b_Amp.sh\r\n".encode())
    #ser.write("i2cset -y -f 7 0x68 0x60 0x03\r\n".encode())
    #time.sleep(0.5)

    ser.write("alsaucm -n -b - << EOM\r\n".encode())
    time.sleep(0.5)
    ser.write("open sa8255-adp-star-snd-card\r\n".encode())
    time.sleep(0.5)
    ser.write("set _verb Record2\r\n".encode())
    time.sleep(0.5)
    ser.write("EOM\r\n".encode())
    time.sleep(0.5)
    ser.write("arecord -Dagm:1,103 -f S16_LE -c 2 -r 48000 /home/root/test_amp_record.wav &\r\n".encode())
    time.sleep(0.5)
    '''
    ser.write("\r\n".encode())
    time.sleep(0.5)
    ser.write("alsaucm -n -b - << EOM\r\n".encode())
    time.sleep(0.5)
    ser.write("open sa8255-adp-star-snd-card\r\n".encode())
    time.sleep(0.5)
    ser.write("set _verb Record2\r\n".encode())
    time.sleep(0.5)
    ser.write("EOM\r\n".encode())
    time.sleep(0.5)
    ser.write("aplay -Dagm:1,0 /data/T01_MENUETTO.wav &\r\n".encode())
    '''
def CAN_send():
    ser.write("echo -e \"0,1,2,3,4,5,6,7,8,9,0,0,0,0,0,0\">/tmp/can_write.txt\r\n".encode())
    ser.write("CAN_Message_Send\r\n".encode())
'''
    while True:
        ser.write("echo -e \"0,1,2,3,4,5,6,7,8,9,0,0,0,0,0,0\">/tmp/can_write.txt\r\n".encode())
        ser.write("CAN_Message_Send\r\n".encode())
        # ser.write("CAN_Reception\r\n".encode())
        time.sleep(3)
        readback()
        if GPIO.event_detected(channel_3):
            print("***CAN cycle stop***")
            break
'''
def reboot():
    ser.write("reboot\r\n".encode())

def usb_mode():
    ser.write("usb_device_mode.sh\r\n".encode())

def I2C_dump():
    ser.write("i2cdump -y -f 7 0x68\r\n".encode())
    time.sleep(0.2)
    readback()
    ser.write("i2cdump -y -f 7 0x69\r\n".encode())
    # ser.write("i2cdetect -a\r\n".encode())

def ctrl_c():
    ser.write("\003\r\n".encode())

def I2C_set():
    ser.write("i2cset -y -f 7 0x68 0x11 0x23\r\n".encode())

def tuner_out_amp():
    ser.write("tuner_out_Amp.sh\r\n".encode())

def tuner_test():
    ser.write("tunertest_client\r\n".encode())
    time.sleep(1)
    readback()
    ser.write("1\r\n".encode())
    time.sleep(0.5)
    readback()
    ser.write("1\r\n".encode())
    time.sleep(0.5)
    readback()
    ser.write("98100\r\n".encode())

def aout_amp_1k():
    ser.write("aout_a2b_Amp.sh T02_1KHZ_SINE_WAVE.wav\r\n".encode())

def lvds_low():
    ser.write("i2cset -y -f 7 0x68 0x30 0x83\r\n".encode())
    time.sleep(1)
    ser.write("i2cset -y -f 7 0x68 0x01 0x00\r\n".encode())
    time.sleep(1)
    ser.write("i2cset -y -f 7 0x69 0x2E 0x83\r\n".encode())
    time.sleep(1)
    ser.write("i2cget -y -f 7 0x69 0x2E\r\n".encode())

def can_echo():
    ser.write("CAN_Echoback\r\n".encode())

def eth_test():
    ser.write("ifconfig eth0 192.168.110.2\r\n".encode())
    '''
    global eth_address
    cmd_eth = "ifconfig eth0 " + eth_address + "\r\n"
    ser.write(cmd_eth.encode())
    time.sleep(0.5)
    readback()
    ser.write("iperf3 -s\r\n".encode())
    '''
def iperf3_s():
    ser.write("iperf3 -s & iperf3 -s -p 5202\r\n".encode())
def iperf3_s_wifi():
    ser.write("iperf3 -s -p 5202\r\n".encode())
def iperf3_s_eth():
    ser.write("iperf3 -s\r\n".encode())
def op_mode_max():
    ser.write("Set_OpMode_Max\r\n".encode())
def wifi_connect():
    ser.write("wifi_connect DHU_5G 12345678\r\n".encode())
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

def power_interrupt():
    GPIO.output(7,1)
    time.sleep(interval_time)
    GPIO.output(7,0)

def update_interval_time():
    global interval_time
    try:
        interval_time = float(interval_entry.get())
        power_interrupt()  # Call power_interrupt() after updating interval_time
    except ValueError:
        messagebox.showerror("数呢哥们？", "你得输个数.")

def toggle_button_power():
    if button_power.config('bg')[-1] == 'orange':
        button_power.config(bg="gray", activebackground="gray")
        GPIO.output(7, 1)
    else:
        button_power.config(bg="orange", activebackground="orange")
        GPIO.output(7, 0)

def toggle_button_reserve():
    global data
    if button_reserve.config('bg')[-1] == 'orange':
        button_reserve.config(bg="gray", activebackground="gray")
    else:
        button_reserve.config(bg="orange", activebackground="orange")
        '''
        with open('/home/javi/leo_share/log.txt', 'a') as log_file:
            log_file.write(data + '\n')
        '''
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
    
    ser.write(data.encode())
    if "lemans:" not in data:
        ser.write("\r\n".encode())
    last_messages.append(data)
    if len(last_messages) > 10:
        last_messages.pop(0)
    current_message_index = -1
    entry.delete(0, tk.END)

def on_key_up(event=None):
    global current_message_index
    if last_messages:
        current_message_index = (current_message_index - 1) % len(last_messages)
        entry.delete(0, tk.END)
        entry.insert(0, last_messages[current_message_index])

def on_key_down(event=None):
    global current_message_index
    if last_messages:
        current_message_index = (current_message_index + 1) % len(last_messages)
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

def ser_i2c_read_command():
    command = "i2cget -y -f " + input1.get() + " 0x" + input2.get() + " 0x" + input3.get() + "\r\n"
    ser.write(command.encode())

def ser_i2c_send_command():
    command = "i2cset -y -f " + input1.get() + " 0x" + input2.get() + " 0x" +input3.get() + " 0x" + input4.get() + "\r\n"
    ser.write(command.encode())

def ser_i2c_dump_command():
    command = "i2cdump -y -f " + input1.get() + " 0x" + input2.get() + "\r\n"
    ser.write(command.encode())

def create_gui():
    global root, text_area
    # Create the main window
    root = tk.Tk()
    root.title("UART Control")
    root.geometry("1200x900")  # Set default window size

    # Create a style for the Notebook tabs
    style = ttk.Style()
    style.configure('TNotebook.Tab', padding=[20, 5], font=('Helvetica', 12))  # Double the padding and font size

    # Create a Notebook widget
    notebook = ttk.Notebook(root, style='TNotebook')
    notebook.pack(expand=True, fill='both')

    # Create the first tab (tag1)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text='tag1')

    # Create the second tab (tag2)
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text='tag2')

    # Add widgets to the first tab (tag1)
    button1 = tk.Button(tab1, text="REBOOT", command=reboot)
    button1.place(x=10, y=10, width=200, height=50)

    button2 = tk.Button(tab1, text="Lemans Login", command=lemans_login)
    button2.place(x=10, y=70, width=200, height=50)

    button3 = tk.Button(tab1, text="A2B Play", command=A2B_play)
    button3.place(x=10, y=130, width=200, height=50)

    button4 = tk.Button(tab1, text="A2B STOP", command=STOP_aout)
    button4.place(x=10, y=190, width=200, height=50)

    button5 = tk.Button(tab1, text="USB DSRC", command=usb_mode)
    button5.place(x=10, y=250, width=200, height=50)

    button6 = tk.Button(tab1, text="A2B Record", command=A2B_record)
    button6.place(x=10, y=310, width=200, height=50)

    button7 = tk.Button(tab1, text="A2B AMP", command=A2B_AMP_play)
    button7.place(x=220, y=70, width=200, height=50)

    button8 = tk.Button(tab1, text="IPERF3 -S", command=iperf3_s)
    button8.place(x=220, y=130, width=200, height=50)

    button9 = tk.Button(tab1, text="PWER INTRPT", command=power_interrupt)
    button9.place(x=220, y=190, width=200, height=50)

    button10 = tk.Button(tab1, text="CAN SEND", command=CAN_send)
    button10.place(x=220, y=250, width=200, height=50)

    button11 = tk.Button(tab1, text="WIFI CONNECT", command=wifi_connect)
    button11.place(x=220, y=310, width=200, height=50)

    button12 = tk.Button(tab1, text="I2C DUMP", command=I2C_dump)
    button12.place(x=430, y=70, width=200, height=50)

    button13 = tk.Button(tab1, text="I2C SET", command=I2C_set)
    button13.place(x=430, y=130, width=200, height=50)

    button14 = tk.Button(tab1, text="TUNER OUT AMP", command=tuner_out_amp)
    button14.place(x=430, y=190, width=200, height=50)

    button15 = tk.Button(tab1, text="TUNER TEST", command=tuner_test)
    button15.place(x=430, y=250, width=200, height=50)

    button16 = tk.Button(tab1, text="TERMINAL", command=terminal)
    button16.place(x=430, y=310, width=200, height=50)

    # Add the copied buttons to the right of the existing buttons
    button17 = tk.Button(tab1, text="OP MODE MAX", command=op_mode_max)
    button17.place(x=640, y=70, width=200, height=50)

    button18 = tk.Button(tab1, text="1KHZ", command=aout_amp_1k)
    button18.place(x=640, y=130, width=200, height=50)

    button19 = tk.Button(tab1, text="CTRL+C", command=ctrl_c)
    button19.place(x=640, y=190, width=200, height=50)

    button20 = tk.Button(tab1, text="ETHERNET", command=eth_test)
    button20.place(x=640, y=250, width=200, height=50)

    button21 = tk.Button(tab1, text="LVDS LOW", command=lvds_low)
    button21.place(x=640, y=310, width=200, height=50)

    button22 = tk.Button(tab1, text="IPERF3 ETH", command=iperf3_s_eth)
    button22.place(x=850, y=70, width=200, height=50)

    button23 = tk.Button(tab1, text="IPERF3 WIFI", command=iperf3_s_wifi)
    button23.place(x=850, y=130, width=200, height=50)

    button24 = tk.Button(tab1, text="CAN ECHOBACK", command=can_echo)
    button24.place(x=850, y=190, width=200, height=50)

    button25 = tk.Button(tab1, text="PLAY A2B2", command=A2B2_play)
    button25.place(x=850, y=250, width=200, height=50)

    button26 = tk.Button(tab1, text="AMP RECORD", command=amp_record)
    button26.place(x=850, y=310, width=200, height=50)

    # Create toggle button
    global button_power
    button_power = tk.Button(tab1, text="POWER", command=toggle_button_power, bg="gray", activebackground="gray")
    button_power.place(x=220, y=10, width=200, height=50)

    global button_reserve
    button_reserve = tk.Button(tab1, text="RESERVE", command=toggle_button_reserve, bg="gray", activebackground="gray")
    button_reserve.place(x=430, y=10, width=200, height=50)

    # Create input field and ENTER button
    global entry
    entry = tk.Entry(tab1)
    entry.place(x=10, y=490, width=600, height=30)
    entry.bind("<Return>", on_enter_click)
    entry.bind("<Up>", on_key_up)  # Bind Page Up key to on_key_up function
    entry.bind("<Down>", on_key_down)  # Bind Page Down key to on_key_down function
    
    enter_button = tk.Button(tab1, text="ENTER", command=on_enter_click)
    enter_button.place(x=620, y=490, width=120, height=30)

    # Create filter1 input field and button
    global filter1_entry, filter1_button
    filter1_entry = tk.Entry(tab1)
    filter1_entry.place(x=10, y=410, width=600, height=30)
    
    filter1_button = tk.Button(tab1, text="IGNORE", command=toggle_filter1, bg="gray", activebackground="gray")
    filter1_button.place(x=620, y=410, width=120, height=30)

    # Create filter2 input field and button
    global filter2_entry, filter2_button
    filter2_entry = tk.Entry(tab1)
    filter2_entry.place(x=10, y=450, width=600, height=30)
    
    filter2_button = tk.Button(tab1, text="REMAIN", command=toggle_filter2, bg="gray", activebackground="gray")
    filter2_button.place(x=620, y=450, width=120, height=30)

    # Create interval time input field and button
    global interval_entry
    interval_entry = tk.Entry(tab1)
    interval_entry.place(x=10, y=370, width=100, height=30)
    
    interval_button = tk.Button(tab1, text="INTERVAL", command=update_interval_time, bg="gray", activebackground="gray")
    interval_button.place(x=120, y=370, width=100, height=30)

    # I2C transit block (tag2)
    global input1, input2, input3, input4
    input1 = tk.Entry(tab2, width=10)
    input1.place(x=10, y=10, width=50, height=30)

    tk.Label(tab2, text="0x").place(x=70, y=14)
    input2 = tk.Entry(tab2, width=10)
    input2.place(x=90, y=10, width=50, height=30)

    tk.Label(tab2, text="0x").place(x=150, y=14)
    input3 = tk.Entry(tab2, width=10)
    input3.place(x=170, y=10, width=50, height=30)

    tk.Label(tab2, text="0x").place(x=230, y=14)
    input4 = tk.Entry(tab2, width=10)
    input4.place(x=250, y=10, width=50, height=30)

    read_button = tk.Button(tab2, text="READ", command=ser_i2c_read_command)
    read_button.place(x=310, y=10, width=100, height=30)

    send_button = tk.Button(tab2, text="SEND", command=ser_i2c_send_command)
    send_button.place(x=420, y=10, width=100, height=30)

    dump_button = tk.Button(tab2, text="DUMP", command=ser_i2c_dump_command)
    dump_button.place(x=530, y=10, width=100, height=30)

    # ETH Address block
    global eth_address
    tk.Label(tab2, text="ETH:").place(x=10, y=50)
    eth_address = tk.Entry(tab2, width=20)
    eth_address.place(x=100, y=50, width=300, height=30)

    # WIFI Address block
    global wifi_address
    tk.Label(tab2, text="WIFI:").place(x=10, y=90)
    wifi_address = tk.Entry(tab2, width=20)
    wifi_address.place(x=100, y=90, width=300, height=30)

    # BT Address block
    global bt_address
    tk.Label(tab2, text="BT:").place(x=10, y=130)
    bt_address = tk.Entry(tab2, width=20)
    bt_address.place(x=100, y=130, width=300, height=30)



    # Create text area for displaying messages
    global text_area
    text_area = ScrolledText(root, height=15, width=113, state=tk.DISABLED)
    text_area.place(x=10, y=560, width=1180, height=250)

    root.after(100, process_queue)  # Start processing the queue

    # Run the GUI event loop
    root.mainloop()



# Run the GUI in a separate thread
gui_thread = threading.Thread(target=create_gui)
gui_thread.daemon = True
gui_thread.start()

while True:
    time.sleep(0.01)
    readback()



