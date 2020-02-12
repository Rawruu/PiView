#!/usr/bin/python3

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
from fpdf import FPDF
from statistics import mean

import serial
import time
import binascii
import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
from datetime import datetime
import PIL
from PIL import ImageTk
from PIL import Image
import os

#have a method for checking if the usb chords are plugged in correctly
#method would write serial command and check for correct response from analyzer
#def check_serial():
        
# Function for converting decimal to binary 
def float_bin(number, places = 3): 
    whole, dec = str(number).split(".")  
    whole = int(whole)  
    dec = int (dec)
    res = bin(whole).lstrip("0b") + "."
  
    for x in range(places):  
        whole, dec = str((decimal_converter(dec)) * 2).split(".")  
        dec = int(dec)  
        res += whole    
    return res  
  
def decimal_converter(num):   
    while num > 1:  
        num /= 10
    return num  
  
def IEEE754(n) : 
  
    # identifying whether the number 
    # is positive or negative
     
    sign = 0
    if n < 0 : 
        sign = 1
        n = n * (-1) 
    p = 30
  
    # convert float to binary 
    dec = float_bin (n, places = p)
  
    # separate the decimal part 
    # and the whole number part 
    whole, dec = str(dec).split(".") 
    whole = int(whole) 
  
    # calculating the exponent(E) 
    exponent = len(str(whole)) - 1
    exponent_bits = 127 + exponent 
  
    # converting the exponent from 
    # decimal to binary 
    exponent_bits = bin(exponent_bits).lstrip("0b") 
  
    # finding the mantissa 
    mantissa = str(whole)[1:exponent + 1] 
    mantissa = mantissa + dec 
    mantissa = mantissa[0:23] 
  
    # the IEEE754 notation in binary 
    final = str(sign) + str(exponent_bits) + mantissa
    byte1 = "0000"+final[0:4]
    byte2 = "0"+final[4:11]
    byte3 = "0"+final[11:18]
    byte4 = "0"+final[18:25]
    byte5 = "0"+final[25:32]
    databyte1 = bytearray([int(byte1,2)])
    databyte2 = bytearray([int(byte2,2)])
    databyte3 = bytearray([int(byte3,2)])
    databyte4 = bytearray([int(byte4,2)])
    databyte5 = bytearray([int(byte5,2)])

    return (databyte1,databyte2,databyte3,databyte4,databyte5)

def write_upperandlower(valueToUpper,valueToLower):
    write_serial_float(bytearray([178]),bytearray([15]),valueToUpper)
    time.sleep(0.08)
    write_serial_float(bytearray([178]),bytearray([16]),valueToLower)

def write_serial_float(command,operand,valueToWrite):
    databytes = IEEE754(valueToWrite)
    
    data = bytearray()
    echo = bytearray()
    #command=bytearray([178])
    #operand =bytearray([15])
    databyte1 = databytes[0]
    databyte2 = databytes[1]
    databyte3 = databytes[2]
    databyte4 = databytes[3]
    databyte5 = databytes[4]
    
    sleepy = 0.05
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0.1)
    
    data = bytearray()
    ser.write(command) #send command byte
    echo = ser.read(10) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte1)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte2)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte3)
    echo = ser.read(10)
    data = data + echo
    
    
    ser.write(databyte4)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte5)
    echo = ser.read(10)
    data = data + echo
    return(data)

    ser.close()

def write_serial_int(n):
    databyte0 = "00000000"
    databyte1 = "00000001"
    databyte2 = "00000010"
    if n==0:
        byte1 = bytearray([int(databyte0,2)])
        byte2 = bytearray([int(databyte0,2)])
        byte3 = bytearray([int(databyte0,2)])
    elif n==1:
        byte1 = bytearray([int(databyte0,2)])
        byte2 = bytearray([int(databyte0,2)])
        byte3 = bytearray([int(databyte1,2)])
    elif n==2:
        byte1 = bytearray([int(databyte0,2)])
        byte2 = bytearray([int(databyte0,2)])
        byte3 = bytearray([int(databyte2,2)])
    
    command=bytearray([162])
    operand =bytearray([4])
    data = bytearray()
    echo = bytearray()
    
    sleepy = 0.05
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0.1)
    
    ser.write(command) #send command byte
    echo = ser.read(10) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(byte1)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(byte2)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(byte3)
    echo = ser.read(10)
    data = data + echo
    print(data)


    ser.close()

# gets O2 data and converts to ppb
def get_O2():
    ser = serial.Serial(
        port='/dev/ttyUSB0',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout = 0)

    sleepy = 0.05
    i=0
    fullcommand = bytearray([1,2,1,0,0,3,13])
    ser.write(fullcommand)
    ser.write(b' ')
    time.sleep(sleepy)
    deldata = ser.read(8)
    data = str(binascii.hexlify(deldata[4:8]))

    c = [data[i:i+2] for i in range (0, len(data), 2)]
    try:
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))
    
        o2_bin = byte1+byte2+byte3+byte4
    
        m = o2_bin[9:]
        mantissa = 0
        mantissa =      (int(m[0])*2**22+int(m[1])*2**21+int(m[2])*2**20+int(m[3])*\
                    2**19+int(m[4])*2**18+int(m[5])*2**17+int(m[6])*2**16+int(m[7])*\
                    2**15+int(m[8])*2**14+int(m[9])*2**13+int(m[10])*2**12+int(m[11])*\
                    2**11+int(m[12])*2**10+int(m[13])*2**9+int(m[14])*2**8+int(m[15])*\
                     2**7+int(m[16])*2**6+int(m[17])*2**5+int(m[18])*2**4+int(m[19])*\
                     2**3+int(m[20])*2**2+int(m[21])*2**1+int(m[22])*2**0)/8388608
                     
        exponent = int(o2_bin[2:9],2)
        sign = (-1)**(int(o2_bin[0],2))
        
        o2_ppm = sign*(2**(exponent-127))*(1+mantissa)
        o2_ppb = 1000*o2_ppm



        ser.close()
    
        return(str(o2_ppb))
    except:
        pass

# gets raw h2o data: need to use raw_to_ppb function to convert to ppb
def get_h20():
    data = bytearray()
    echo = bytearray()
    command=bytearray([146])
    operand =bytearray([1])
    sleepy = 0.05
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0.05)
    
    data = bytearray()
    ser.write(command) #send command byte
    echo = ser.read(10) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    echo = ser.read(10)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    echo = ser.read(10)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    echo = ser.read(10)
    data = data + echo
    
    
    ser.write(bytearray([echo[-1]]))
    echo = ser.read(10)
    data = data + echo
    return(data)

    ser.close()

# converts raw h2o data to ppb
def raw_to_ppb (data):
    raw_hex = str(binascii.hexlify(data[2:]))
    c = [raw_hex[i:i+2] for i in range (0, len(raw_hex), 2)]
    try:
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))
        byte5 = "{:08b}".format(int(c[5], base=16))
    
        h20_bin = byte1+byte2+byte3+byte4+byte5
    
        m1 = h20_bin[14:16]
        m2 = h20_bin[17:24]
        m3 = h20_bin[25:32]
        m4 = h20_bin[33:40]
        m = m1+m2+m3+m4
            
        mantissa =      (int(m[0])*2**22+int(m[1])*2**21+int(m[2])*2**20+int(m[3])*\
                    2**19+int(m[4])*2**18+int(m[5])*2**17+int(m[6])*2**16+int(m[7])*\
                    2**15+int(m[8])*2**14+int(m[9])*2**13+int(m[10])*2**12+int(m[11])*\
                    2**11+int(m[12])*2**10+int(m[13])*2**9+int(m[14])*2**8+int(m[15])*\
                     2**7+int(m[16])*2**6+int(m[17])*2**5+int(m[18])*2**4+int(m[19])*\
                     2**3+int(m[20])*2**2+int(m[21])*2**1+int(m[22])*2**0)/8388608
        
        e1 = h20_bin[5:8]
        e2 = h20_bin[9:14]
        e = e1+e2
        exponent = int(e,2)
        sign = (-1)**(int(h20_bin[4],2))
        
        h20_ppb = sign*(2**(exponent-127))*(1+mantissa)
    
        return(str(h20_ppb))
    except:
        pass





#####GUI
LARGEST_FONT = ("Century Gothic", 20, 'bold')
LARGE_FONT = ("Century Gothic", 14, 'bold')
SMALL_FONT = ("Century Gothic", 8)
style.use("ggplot")

f1 = Figure(figsize=(4,3),dpi=100)
f2 = Figure(figsize=(4,3),dpi=100)
a1 = f1.add_subplot(111)
a2 = f2.add_subplot(111)
f2.subplots_adjust(left=0.25, right=0.9, bottom =0.2, top=0.9)
f1.subplots_adjust(left=0.25, right=0.9, bottom =0.2, top=0.9)
o2_dataList = ""
h2o_dataList = ""
recording=False
start_time=datetime.now()
global start_timee
start_timee = start_time.strftime("%m_%d_%y_%I:%M:%S")
## All the field names for test details

#RPiReader class unpacks and shows pages. Also holds the window title and icon. Any new pages need to be added to self.frames{}

class RPiReader(tk.Tk):
    def __init__(self, *args, **kwargs): #args are variables. kwargs are keyboard args (dictionarys and such)
    
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self,default="insert qam icon") #create .ico for qam icon
        tk.Tk.wm_title(self, "Pi-View")
        
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = { }
        
        for F in (Splash, StartPage, PageOne, PageTwo):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky="nsew")
        
        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

class Splash(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SPLASH SCREEN... put a big logo here", font=LARGE_FONT)
        label.grid(row=1,column=1)
        label.config(bg="grey25")
        
        self.gambar = Image.open('QAM Logo.jpg')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash)
        self.img.image = self.imgSplash
        self.img.grid(row=2,column=1,columnspan=4,rowspan=15)
        
        
        button1 = ttk.Button(self, text="Enter", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=3,column=4)
        
        


#StartPage appears first. contains

        
class StartPage(tk.Frame):
    recording = False
    
    def start_show_test(self, controller):
        controller.show_frame(PageOne)
        self.record()
        
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="Field Screen", font=LARGEST_FONT)
        label1.grid(row=1,column=1, columnspan=3, sticky=N)
        label1.config(bg="grey25", fg="#7fa6a3")
        
        self.configure(background="grey25")
        
        self.gambar = Image.open('qam_logo_transparent(2).png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        self.img.grid(row=16,column=4,rowspan = 4, sticky=S)
        
        button1 = tk.Button(self, text="Testing Screen",bg="grey15",fg="grey75",font=LARGE_FONT, command=lambda: controller.show_frame(PageOne))
        button1.grid(row=3,column=4)
        
        #Start Recording Button => starts the record() function                 try to make one button that will show the testing screen and start a test
        #button2 = ttk.Button(self, text="Start Recording", command=self.record)
        #button2.grid(row=2,column=4)
        
        
        #exit button
        #button4 = ttk.Button(self, text="Exit", command=quit)
        #button4.grid(row=5,column=3)
        
        #global header_list
        #header_list = ['test title','client','test gas','source gas','tect','sys flow','comments','D serial','D cal date','D flow','D spec','M serial','M cal date','M flow','M spec']
        
        with open('Header_default.csv', newline='') as t:
                headreader = csv.reader(t)
                global header_list
                header_list = []
                for row in headreader:
                        header_list.append(row[0])
        
        paddx = 2
        paddy = 2
        
        ####Document fields (title, client, etc)
        # title entry
        label3 = tk.Label(self, text="Test Point ID:", font=SMALL_FONT)
        label3.grid(row=2,column=1, padx=paddx,pady=paddy)
        label3.config(bg="grey25",fg="white")
        
        global title
        self.title = StringVar(self, value=header_list[0])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.title)
        self.textbox.grid(row=3,column=1, padx=paddx,pady=paddy)
        title = self.title
        
        # client entry
        label4 = tk.Label(self, text="Client:", font=SMALL_FONT)
        label4.grid(row=4,column=1, padx=paddx,pady=paddy)
        label4.config(bg="grey25",fg="white")
        
        global client
        self.client = StringVar(self, value=header_list[1])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.client)
        self.textbox.grid(row=5,column=1, padx=paddx,pady=paddy)
        client = self.client
        
        # test gas entry
        label5 = tk.Label(self, text="Test Gas:", font=SMALL_FONT)
        label5.grid(row=6,column=1, padx=paddx,pady=paddy)
        label5.config(bg="grey25",fg="white")
        
        global test_gas
        self.test_gas = StringVar(self, value=header_list[2])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.test_gas)
        self.textbox.grid(row=7,column=1, padx=paddx,pady=paddy)
        test_gas = self.test_gas
        
        # source gas entry
        label6 = tk.Label(self, text="Source Gas:", font=SMALL_FONT)
        label6.grid(row=8,column=1, padx=paddx,pady=paddy)
        label6.config(bg="grey25",fg="white")
        
        global source_gas
        self.source_gas = StringVar(self, value=header_list[3])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.source_gas)
        self.textbox.grid(row=9,column=1, padx=paddx,pady=paddy)
        source_gas = self.source_gas
        
        # technician entry
        label7 = tk.Label(self, text="Technician:", font=SMALL_FONT)
        label7.grid(row=10,column=1, padx=paddx,pady=paddy)
        label7.config(bg="grey25",fg="white")
        
        global technician
        self.technician = StringVar(self, value=header_list[4])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.technician)
        self.textbox.grid(row=11,column=1, padx=paddx,pady=paddy)
        technician = self.technician
        
        # system flow entry
        label8 = tk.Label(self, text="System Flow:", font=SMALL_FONT)
        label8.grid(row=12,column=1, padx=paddx,pady=paddy)
        label8.config(bg="grey25",fg="white")
        
        global system_flow
        self.system_flow = StringVar(self, value=header_list[5])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.system_flow)
        self.textbox.grid(row=13,column=1, padx=paddx,pady=paddy)
        system_flow = self.system_flow
        
        #comments entry
        label9 = tk.Label(self, text="Comments:", font=SMALL_FONT)
        label9.grid(row=14,column=1, padx=paddx,pady=paddy)
        label9.config(bg="grey25",fg="white")
        
        global comments
        self.comments = StringVar(self, value=header_list[6])
        self.textbox = ttk.Entry(self,width=40, textvariable = self.comments)
        self.textbox.grid(row=15,column=1, padx=paddx,pady=paddy)
        comments = self.comments
        
        ### analyser info entries
        ## delta f info entry
        #deltaf serial number entry
        label10 = tk.Label(self, text="Delta F", font=LARGE_FONT)
        label10.grid(row=2,column=2, padx=paddx,pady=paddy)
        label10.config(bg="grey25", fg="#7fa6a3")
        
        label10 = tk.Label(self, text="Instrument Serial #:", font=SMALL_FONT)
        label10.grid(row=3,column=2, padx=paddx,pady=paddy)
        label10.config(bg="grey25",fg="white")
        
        global deltaf_serial
        self.deltaf_serial = StringVar(self, value=header_list[7])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_serial)
        self.textbox.grid(row=4,column=2, padx=paddx,pady=paddy)
        deltaf_serial = self.deltaf_serial
        
        #deltaf calibration date entry
        label11 = tk.Label(self, text="Instrument Calibration Date:", font=SMALL_FONT)
        label11.grid(row=5,column=2, padx=paddx,pady=paddy)
        label11.config(bg="grey25",fg="white")
        
        global deltaf_cal
        self.deltaf_cal = StringVar(self, value=header_list[8])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_cal)
        self.textbox.grid(row=6,column=2, padx=paddx,pady=paddy)
        deltaf_cal = self.deltaf_cal
        
        #instrument flow entry
        label12 = tk.Label(self, text="Instrument Flow:", font=SMALL_FONT)
        label12.grid(row=7,column=2, padx=paddx,pady=paddy)
        label12.config(bg="grey25",fg="white")
        
        global deltaf_flow
        self.deltaf_flow = StringVar(self, value=header_list[9])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_flow)
        self.textbox.grid(row=8,column=2, padx=paddx,pady=paddy)
        deltaf_flow = self.deltaf_flow
        
        #instrument specification
        label13 = tk.Label(self, text="Specification", font=SMALL_FONT)
        label13.grid(row=9,column=2, padx=paddx,pady=paddy)
        label13.config(bg="grey25",fg="white")
        
        global deltaf_spec
        self.deltaf_spec = StringVar(self, value=header_list[10])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_spec)
        self.textbox.grid(row=10,column=2, padx=paddx,pady=paddy)
        deltaf_spec = self.deltaf_spec
        
        ## tracer2 info entry
        #tracer2 serial number entry
        label10 = tk.Label(self, text="Meeco Tracer2", font=LARGE_FONT)
        label10.grid(row=2,column=3, padx=paddx,pady=paddy)
        label10.config(bg="grey25", fg="#7fa6a3")
        
        label10 = tk.Label(self, text="Instrument Serial #:", font=SMALL_FONT)
        label10.grid(row=3,column=3, padx=paddx,pady=paddy)
        label10.config(bg="grey25",fg="white")
        
        global tracer_serial
        self.tracer_serial = StringVar(self, value=header_list[11])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_serial)
        self.textbox.grid(row=4,column=3, padx=paddx,pady=paddy)
        tracer_serial = self.tracer_serial
        
        #tracer2 calibration date entry
        label11 = tk.Label(self, text="Instrument Calibration Date:", font=SMALL_FONT)
        label11.grid(row=5,column=3, padx=paddx,pady=paddy)
        label11.config(bg="grey25",fg="white")
        
        global tracer_cal
        self.tracer_cal = StringVar(self, value=header_list[12])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_cal)
        self.textbox.grid(row=6,column=3, padx=paddx,pady=paddy)
        tracer_cal = self.tracer_cal
        
        #instrument flow entry
        label12 = tk.Label(self, text="Instrument Flow:", font=SMALL_FONT)
        label12.grid(row=7,column=3, padx=paddx,pady=paddy)
        label12.config(bg="grey25",fg="white")
        
        global tracer_flow
        self.tracer_flow = StringVar(self, value=header_list[13])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_flow)
        self.textbox.grid(row=8,column=3, padx=paddx,pady=paddy)
        tracer_flow = self.tracer_flow
        
        #instrument specification
        label13 = tk.Label(self, text="Specification", font=SMALL_FONT)
        label13.grid(row=9,column=3, padx=paddx,pady=paddy)
        label13.config(bg="grey25",fg="white")
        
        global tracer_spec
        self.tracer_spec = StringVar(self, value=header_list[14])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_spec)
        self.textbox.grid(row=10,column=3, padx=paddx,pady=paddy)
        tracer_spec = self.tracer_spec
        
        #current o2
        label13 = tk.Label(self, text="Current O2:", font=LARGE_FONT)
        label13.grid(row=13,column=2, padx=paddx,pady=paddy)
        label13.config(bg="grey25",fg="white")
        
        global currento2
        currento2 = StringVar(value=0)
        label14 = tk.Label(self,textvariable=currento2, width=20,bg="grey35",fg="white", font=SMALL_FONT)
        label14.grid(row=14, column=2, padx=paddx,pady=paddy)
        
        #current h2o
        label13 = tk.Label(self, text="Current H2O:", font=LARGE_FONT)
        label13.grid(row=13,column=3, padx=paddx,pady=paddy)
        label13.config(bg="grey25",fg="white")
        
        global currenth2o
        currenth2o = StringVar(value=0)
        label14 = tk.Label(self,textvariable=currenth2o, width=20,bg="grey35",fg="white", font=SMALL_FONT)
        label14.grid(row=14, column=3, padx=paddx,pady=paddy)
        
        
        
        self.upper_band = DoubleVar(self)
        self.textbox = ttk.Entry(self,width=20, textvariable = self.upper_band)
        self.textbox.grid(row=3,column=5, padx=paddx,pady=paddy)
        
        
        self.lower_band = DoubleVar(self)
        self.textbox = ttk.Entry(self,width=20, textvariable = self.lower_band)
        self.textbox.grid(row=3,column=6, padx=paddx,pady=paddy)

        button1 = tk.Button(self, text="Set Bands",bg="grey15",fg="grey75",font=LARGE_FONT, command=lambda: write_upperandlower(self.upper_band.get(),self.lower_band.get()))
        button1.grid(row=4,column=5,columnspan=2)
        
        label14 = tk.Label(self,text="Upper Band:", width=20,bg="grey35",fg="white", font=SMALL_FONT)
        label14.grid(row=2, column=5, padx=paddx,pady=paddy)
        
        label14 = tk.Label(self,text="Lower Band:", width=20,bg="grey35",fg="white", font=SMALL_FONT)
        label14.grid(row=2, column=6, padx=paddx,pady=paddy)
        
        button1 = tk.Button(self, text="Service Mode",bg="grey15",fg="grey75",font=LARGE_FONT, command=lambda: write_serial_int(0))
        button1.grid(row=5,column=5)
        
        button1 = tk.Button(self, text="Inert Mode",bg="grey15",fg="grey75",font=LARGE_FONT, command=lambda: write_serial_int(1))
        button1.grid(row=5,column=6)
        
        

        

class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graphing Page", font=LARGEST_FONT)
        label.config(bg="grey25", fg="#7fa6a3")
        label.grid(row=1,column=1,columnspan=2)
        
        self.configure(background="grey25")
        
        global directory
        directory = '/home/pi/Desktop/JoelPi'
        
        global o2data_max
        global o2data_min
        self.o2data_max = 0
        self.o2data_min = 0
        
        #Oxygen DeltaF Graph
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=2,column=1,rowspan=6)
        
        #Moisture Tracer Graph
        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=2,column=2,rowspan=6)
        
        #toolbar = NavigationToolbar2Tk(canvas1,self)
        #toolbar.update()
        #canvas1._tkcanvas.grid(row=3,column=1)
        
        #toolbar = NavigationToolbar2Tk(canvas2,self)
        #toolbar.update()
        #canvas2._tkcanvas.grid(row=3,column=2)
        
        #Stop Recording Button => starts the stop() function
        button3 = tk.Button(self, text="Stop Recording",bg="grey15",fg="grey85",width=20, command=self.stop)
        button3.grid(row=5,column=3, pady=3, padx=2)
        
        #Start Recording Button => starts the record() function
        button2 = tk.Button(self, text="Start Recording",bg="grey15",fg="grey85",width=20, command=self.record)
        button2.grid(row=4,column=3, pady=3, padx=2)
        
        button1 = tk.Button(self, text="Back",bg="grey15",fg="grey85",width=20, command=lambda: controller.show_frame(StartPage))
        button1.grid(row=6,column=3, pady=3, padx=2)
        
        button2 = tk.Button(self, text="PDF",bg="grey15",fg="grey85",width=20, command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=7,column=3, pady=3, padx=2)
        
        #button2 = tk.Button(self, text="Select File Location",bg="grey15",fg="grey85",width=20, command=self.choose_directory)
        #button2.grid(row=3,column=3, pady=3, padx=2)
        
        self.label15 = tk.Label(self, text="IDLE", bg="IndianRed",fg="grey85",width=20,height=2, font=('Century Gothic',10,'bold'))
        self.label15.grid(row=2,column=3, pady=3, padx=2)
        
        self.gambar = Image.open('qam_logo_transparent(2).png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        self.img.grid(row=9,column=5, rowspan=3 , sticky=S)
        
        #current o2
        label13 = tk.Label(self, text="Current O2:", font=LARGE_FONT)
        label13.grid(row=9,column=1)
        label13.config(bg="grey25",fg="white")
        
        label14 = tk.Label(self,textvariable=currento2, width=20,bg="grey35",fg="white", font=SMALL_FONT)
        label14.grid(row=10, column=1)
        
        #current h2o
        label13 = tk.Label(self, text="Current H2O:", font=LARGE_FONT)
        label13.grid(row=9,column=2)
        label13.config(bg="grey25",fg="white")
        
        label14 = tk.Label(self,textvariable=currenth2o, width=20,bg="grey35",fg="white", font=SMALL_FONT)
        label14.grid(row=10, column=2)
        
        
    def idle_on_off(self):
        if self.label15['text'] == 'IDLE':
            self.label15.configure(text="RECORDING", bg="#7fa6a3")
        else:
            self.label15.configure(text="IDLE", bg="IndianRed")
        
    def choose_directory(self):
        global directory
        directory = filedialog.askdirectory()
    
    
        
### Start Recording function: writes o2, h20, and time variables to csv files        
    def record(self):
        PageOne.idle_on_off(self)
        global recording
        red_green = 'green'
        on_off = "Recording"
        recording=True
        self.headerFileTitle = str(client.get()) + "_" + str(title.get()) + "_Header_" + start_timee
        path = directory + '/' + str(client.get()) + "_" + str(title.get()) + start_timee +"{}"
        global header_list
        header_list =[]
        header_list.append(title.get())
        header_list.append(client.get())
        header_list.append(test_gas.get())
        header_list.append(source_gas.get())
        header_list.append(technician.get())
        header_list.append(system_flow.get())
        header_list.append(comments.get())
        header_list.append(deltaf_serial.get())
        header_list.append(deltaf_cal.get())
        header_list.append(deltaf_flow.get())
        header_list.append(deltaf_spec.get())
        header_list.append(tracer_serial.get())
        header_list.append(tracer_cal.get())
        header_list.append(tracer_flow.get())
        header_list.append(tracer_spec.get())
        
        i=0
        while os.path.exists(path.format(str(i))):
                i=int(i)+1
        else:
                os.mkdir(path.format(str(i)))
                global pathF
                pathF=str(path.format(str(i)))
        with open(os.path.join(path.format(str(i)),self.headerFileTitle)+'.csv', 'w+', newline='') as c:
            writer3 = csv.writer(c)
            writer3.writerow([title.get()])
            writer3.writerow([client.get()])
            writer3.writerow([test_gas.get()])
            writer3.writerow([source_gas.get()])
            writer3.writerow([technician.get()])
            writer3.writerow([system_flow.get()])
            writer3.writerow([comments.get()])
            writer3.writerow([deltaf_serial.get()])
            writer3.writerow([deltaf_cal.get()])
            writer3.writerow([deltaf_flow.get()])
            writer3.writerow([deltaf_spec.get()])
            writer3.writerow([tracer_serial.get()])
            writer3.writerow([tracer_cal.get()])
            writer3.writerow([tracer_flow.get()])
            writer3.writerow([tracer_spec.get()])
            writer3.writerow([start_timee])
            c.flush()
            
            
    def stop(self):
        global recording
        recording = False
        PageOne.idle_on_off(self)
        stop_time= datetime.now()
        
        global o2MeanValue
        o2MeanValue = str(mean(o2Valuelist))
        global o2MaxValue
        o2MaxValue = str(max(o2Valuelist))
        global o2FinalValue
        o2FinalValue = str(o2Valuelist[-1])
        
        global h2oMeanValue
        h2oMeanValue = str(mean(h2oValuelist))
        global h2oMaxValue
        h2oMaxValue = str(max(h2oValuelist))
        global h2oFinalValue
        h2oFinalValue = str(h2oValuelist[-1])
        
        self.headerFileTitle = str(client.get()) + "_" + str(title.get()) + "_Header_" + start_timee
        path = directory + '/' + str(title.get())
        with open(os.path.join(pathF,self.headerFileTitle)+'.csv', 'a', newline='') as c:
            writer3 = csv.writer(c)
            writer3.writerow([stop_time])
            writer3.writerow([o2MeanValue])
            writer3.writerow([o2MaxValue])
            writer3.writerow([o2FinalValue])
            writer3.writerow([h2oMeanValue])
            writer3.writerow([h2oMaxValue])
            writer3.writerow([h2oFinalValue])
            c.close()
            
            
            
        with open('/home/pi/Desktop/JoelPi/Header_default.csv', 'w+',newline='') as d:
            writer4 = csv.writer(d)
            for row in header_list:
                writer4.writerow([row])
            d.close()
            
            
            
    def animateo2(self):
        while True:
                try:
                        o2 = get_O2()
                        o2 = round(float(o2),2)
                        break
                except:
                        time.sleep(1)
                
        currento2.set(o2)
        
        try:
                if o2data_max<o2:
                        o2data_max = o2
                if o2data_min>o2:
                        o2data_min = o2
        except:
                o2data_max = 0
                o2data_min = 0
                if o2data_max<o2:
                        o2data_max = o2
                if o2data_min>o2:
                        o2data_min = o2
        o2time = datetime.now()-start_time
        global o2_dataList
        o2_dataList = o2_dataList + '\n' + str(round((o2time.total_seconds())/60,2))+ ',' + str(o2)
        o2dataList = o2_dataList.split('\n')
        o2dataList.pop(0)
        #print(o2dataList)
        o2xList = []
        o2yList = []
        for eachLine in o2dataList:
            if len(str(eachLine)) > 1:
                x1, y1 = eachLine.split(',')
                o2xList.append(float(x1))
                o2yList.append(float(y1))
        a1.clear()
        a1.ticklabel_format(useOffset=False)
        
        a1.set_ylim(min((0, o2data_min+o2data_min*0.1)), max((10, o2data_max+o2data_max*0.1)))
        a1.plot(o2xList,o2yList)
        a1.set_title("Oxygen (ppb) vs Time (minutes)")
        a1.set_xlabel('Time (minutes)')
        a1.set_ylabel('Oxygen (ppb)')
        
        o2fileTitle = str(client.get()) + "_" + str(title.get()) + "_O2_" + start_timee
        
        if recording == True:
            global o2Valuelist
            o2Valuelist = []
            with open(os.path.join(pathF,o2fileTitle)+'.csv', 'w+', newline='') as o:
                writer1 = csv.writer(o, escapechar=' ',quoting=csv.QUOTE_NONE)
                for eachLine in o2dataList:
                        writer1.writerow([eachLine])
                        everyLine = eachLine.split(",")
                        o2Valuelist.append(float(everyLine[1]))
                #print(o2Valuelist)
                
                o.flush()

    def animateh2o(j):
        while True:
                try:
                        h2o = raw_to_ppb(get_h20())
                        h2o = round(float(h2o),2)
                        break
                except:
                        time.sleep(1)
                
        
        if h2o<0:
                h2o=0
        currenth2o.set(h2o)
                
                
        try:
                if h2odata_max<h2o:
                        h2odata_max = h2o
                if h2odata_min>h2o:
                        h2odata_min = h2o
        except:
                h2odata_max = 0
                h2odata_min = 0
                if h2odata_max<h2o:
                        h2odata_max = h2o
                if h2odata_min>h2o:
                        h2odata_min = h2o
        h2otime = datetime.now()-start_time
        global h2o_dataList
        h2o_dataList = h2o_dataList + '\n' + str(round((h2otime.total_seconds())/60,2))+ ',' + str(h2o)
        h2odataList = h2o_dataList.split('\n')
        h2odataList.pop(0)
        h2oxList = []
        h2oyList = []
        for eachLine in h2odataList:
            if len(str(eachLine)) > 1:
                x2, y2 = eachLine.split(',')
                h2oxList.append(float(x2))
                h2oyList.append(float(y2))
        a2.clear()
        a2.ticklabel_format(useOffset=False)
        a2.set_ylim(min((0, h2odata_min+h2odata_min*0.1)), max((10, h2odata_max+h2odata_max*0.1)))
        a2.plot(h2oxList, h2oyList)
        a2.set_title("Moisture (ppb) vs Time (minutes)")
        a2.set_xlabel('Time (minutes)')
        a2.set_ylabel('Moisture (ppb)')
        
        h2ofileTitle = str(client.get()) + "_" + str(title.get()) + "_H2O_" + start_timee
        
        
        if recording == True:
            global h2oValuelist
            h2oValuelist = []
            with open(os.path.join(pathF,h2ofileTitle)+'.csv', 'w+', newline='') as h:
                writer2 = csv.writer(h, escapechar=' ',quoting=csv.QUOTE_NONE)
                for eachLine in h2odataList:
                        writer2.writerow([eachLine])
                        everyLine = eachLine.split(",")
                        h2oValuelist.append(float(everyLine[1]))
                
                h.flush()
   


        

class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(background="grey25")
        
        Label(self, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=69,y=108)
        Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=450, y=102)
        Label(self, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=75,y=188)
        Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=450, y=185)
        button1 = tk.Button(self, text="Back",bg="grey15",fg="grey85",width=20, command=lambda: controller.show_frame(StartPage))
        button1.place(height = 50, width=125, x=800, y=102)

        # Note for the user to ensure proper input
        Label(self, text='NOTE: You must add ".pdf" to the end of your saved filename.', font=("Century Gothic",10, "italic"), bg="Grey25", fg="Orange", width=75, justify="center").place(x=0,y=375)

        # Generate PDF default/greyed out
        Button(self, text="Generate PDF", bg="Grey50", fg="White", font=("Century Gothic", 17, "bold"), state="disabled").place(height=75, width=450, x=75, y=277)
        
        global var1
        var1 = StringVar()

        global img1
        img1 = PhotoImage(file="Letterhead_Logo.gif")
        
        

        def buttonClick():
            print("Success!!")

        def h2oinfo():
            print("H2O info selected")
            Label(top1, text="The information file has been attached!", font=('Century Gothic',17), fg="green2", bg="grey25").place(x=575,y=310)

        def o2info():
            print("O2 info selected")
            Label(top2, text="The information file has been attached!", font=('Century Gothic',17), fg="green2", bg="grey25").place(x=575,y=310)

        def h2o_selected():
            print(var1.get())
            Label(self, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="DeepSkyBlue", justify="right").place(x=69,y=108)
            Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open1).place(height=50, width=125, x=450, y=102)
            Label(self, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=75,y=188)
            Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=450, y=185)

        def o2_selected():
            print(var1.get())
            Label(self, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="SpringGreen3", justify="right").place(x=75,y=188)
            Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open2).place(height=50, width=125, x=450, y=185)
            Label(self, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=69,y=108)
            Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=450, y=102)

        def both_selected():
            print(var1.get())
            Label(self, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="DeepSkyBlue", justify="right").place(x=69,y=108)
            Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open1).place(height=50, width=125, x=450, y=102)
            Label(self, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="SpringGreen3", justify="right").place(x=75,y=188)
            Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open2).place(height=50, width=125, x=450, y=185)

        s1 = ttk.Style()
        s1.configure("h2o.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="#00BFFF")
        s1.configure("o2.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="#00CD66")
        s1.configure("both.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="Orange")

        # Radiobuttons
        rad_h2o = ttk.Radiobutton(self, text="H2O", style="h2o.TRadiobutton", variable=var1, value="radH2O", command=h2o_selected).place(x=105, y=35)
        rad_o2 = ttk.Radiobutton(self, text="O2", style="o2.TRadiobutton", variable=var1, value="radO2", command=o2_selected).place(x=270, y=35)
        rad_both = ttk.Radiobutton(self, text="Both", style="both.TRadiobutton", variable=var1, value="radBoth", command=both_selected).place(x=420, y=35)

        ####### FILEPATH FUNCTIONS #######
        # This prompts the user to open the first CSV or TXT file
        def open1():
            global filepath1
            filepath1 = filedialog.askopenfilename(initialdir="/Desktop", title="Select a file", filetypes=(("csv files","*.csv"),("txt files","*.txt")))
            print(filepath1)
            if filepath1:
                global top1
                top1=Toplevel()
                top1.geometry("1040x520")
                top1.resizable(False,False)
                top1.config(bg="Grey25")
                filepath1a = filepath1.replace('H2O','Header')
                global ff1
                global aa1
                global xx1
                global yy1
                ff1 = Figure(figsize=(5,5), dpi=100)
                aa1 = ff1.add_subplot(111)
                xx1 = []
                yy1 = []
                global H2odata_min
                global H2odata_max
                H2odata_min = 0
                H2odata_max = 0
                with open(filepath1a, newline ='') as hcsvfile:
                        hheader = csv.reader(hcsvfile)
                        global hheaderlist
                        hheaderlist = []
                        for row in hheader:
                                hheaderlist.append(row[0])
                with open(filepath1, newline = '') as csvfile:
                    plots= csv.reader(csvfile, delimiter=',')
                    for row in plots:
                        xx1.append(float(row[0]))
                        yy1.append(float(row[1]))
                        if float(row[1]) < H2odata_min:
                                H2odata_min = float(row[1])
                        if float(row[1]) > H2odata_max:
                                H2odata_max = float(row[1])
                aa1.ticklabel_format(useOffset=False)        
                aa1.set_ylim(min((0, H2odata_min+H2odata_min*0.1)), max((10, H2odata_max+H2odata_max*0.1)))
                aa1.set_title("Moisture (ppb) over Time (minutes)")
                aa1.set_xlabel('Time (minutes)')
                aa1.set_ylabel('Moisture (ppb)')
                aa1.plot(xx1, yy1, color='blue', marker='o')
                aa1.grid(True)

                global h2oMeanvalue
                h2oMeanvalue = str(round(mean(yy1),2))
                global h2oMaxvalue
                h2oMaxvalue = str(round(max(yy1),2))
                global h2oFinalvalue
                h2oFinalvalue = str(round(yy1[-1],2))



                canvas = FigureCanvasTkAgg(ff1, master=top1)
                canvas.get_tk_widget().place(x=10,y=10)
                ff1.savefig('h2opdfplt.png', bbox_inches='tight')
                def confirmH2O():
                    print("H2O Comfirmed!")
                    if var1.get() == "radH2O":
                        print("Export H2O only")
                        Label(self, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=580, y=114)
                        Button(self, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportH2O).place(height=75, width=450, x=75, y=277)
                    else:
                        print("Export Both")
                        Label(self, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=580, y=114)
                        Button(self, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportBoth).place(height=75, width=450, x=75, y=277)
                    top1.destroy()

                def cancelH2O():
                    print("H2O Cancelled.")
                    Label(self, text="Done!", font=('Century Gothic',10,'bold'), fg="Grey25", bg="Grey25").place(x=580, y=114)
                    Button(self, text="Generate PDF", bg="Grey50", fg="White", font=("Century Gothic", 17, "bold"), state="disabled").place(height=75, width=450, x=75, y=277)
                    top1.destroy()

                Button(top1, text="Cancel", fg="white", bg="IndianRed", font=('Century Gothic',17,'bold'), command=cancelH2O).place(height=100, width=250, x=520, y=410)
                Button(top1, text="Confirm", fg="white", bg="SpringGreen3", font=('Century Gothic',17,'bold'), command=confirmH2O).place(height=100, width=250, x=780, y=410)
                Label(top1, text="Ensure that you selected the correct file by checking the file path, below:", fg="Orange", bg="Grey25", font=("Century Gothic",10, "bold"), justify="center").place(x=540, y=10)
                Label(top1, text=filepath1, fg="Grey85", bg="Grey25", width=66, justify="center", wraplength=500).place(x=540, y=30)
                Label(top1, text="Attach the H2O information file:", fg="White", bg="Grey25", font=("Century Gothic",20,"bold"), wraplength="300").place(x=555, y=180)
                Button(top1, text="Open", fg="white", bg="Grey50", font=('Century Gothic',17,'bold'), command=h2oinfo).place(width=170, height=75, x=820, y=175)
                Label(top2, text="Average:", fg="white",bg="grey25",font=SMALL_FONT).place(x=520,y=300)
                Label(top2, text=h2oMeanvalue, fg="white",bg="grey15",font=SMALL_FONT).place(x=580,y=300, width=40)
                Label(top2, text="Maximum:", fg="white",bg="grey25",font=SMALL_FONT).place(x=520, y=320)
                Label(top2, text=h2oMaxvalue, fg="white",bg="grey15",font=SMALL_FONT).place(x=580, y=320, width=40)
                Label(top2, text="Final:", fg="white",bg="grey25",font=SMALL_FONT).place(x=520, y=340)
                Label(top2, text=h2oFinalvalue, fg="white",bg="grey15",font=SMALL_FONT).place(x=580, y=340, width=40)

            # This clears the error that would orccur if the user clicked cancel
            else:
                print("Nothing Selected.")

        # This prompts the user to open the second CSV or TXT file
        def open2():
            global filepath2
            filepath2 = filedialog.askopenfilename(initialdir="/Desktop", title="Select a file", filetypes=(("csv files","*.csv"),("txt files","*.txt")))
            if filepath2:
                global top2
                top2=Toplevel()
                top2.geometry("1040x520")
                top2.resizable(False,False)
                top2.config(bg="Grey25")
                filepath1b = filepath2.replace('O2','Header')
                global ff2
                global aa2
                global xx2
                global yy2
                ff2 = Figure(figsize=(5,5), dpi=100)
                aa2 = ff2.add_subplot(111)
                xx2 = []
                yy2 = []
                global O2data_min
                global O2data_max
                O2data_min = 0
                O2data_max = 0
                with open(filepath1b, newline ='') as ocsvfile:
                        oheader = csv.reader(ocsvfile)
                        global oheaderlist
                        oheaderlist = []
                        for row in oheader:
                                oheaderlist.append(row[0])
                with open(filepath2, newline = '') as csvfile:
                    plots= csv.reader(csvfile)
                    for row in plots:
                        xx2.append(float(row[0]))
                        yy2.append(float(row[1]))
                        if float(row[1]) < O2data_min:
                                O2data_min = float(row[1])
                        if float(row[1]) > O2data_max:
                                O2data_max = float(row[1])
                aa2.ticklabel_format(useOffset=False)
                aa2.set_ylim(min((0, O2data_min+O2data_min*0.1)), max((10, O2data_max+O2data_max*0.1)))
                aa2.set_title("Oxygen (ppb) over Time (minutes)")
                aa2.set_xlabel('Time (minutes)')
                aa2.set_ylabel('Oxygen (ppb)')
                aa2.plot(xx2, yy2, color='green', marker='o')
                aa2.grid(True)
                
                global o2Meanvalue
                o2Meanvalue = str(round(mean(yy2),2))
                global o2Maxvalue
                o2Maxvalue = str(round(max(yy2),2))
                global o2Finalvalue
                o2Finalvalue = str(round(yy2[-1],2))

                canvas = FigureCanvasTkAgg(ff2, master=top2)
                canvas.get_tk_widget().place(x=10,y=10)
                ff2.savefig('o2pdfplt.png', bbox_inches='tight')
                def confirmO2():
                    print("O2 Confirmed!")
                    if var1.get() == "radO2":
                        # This redirects to the exportO2 function so only the O2 file is used
                        Label(self, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=580, y=197)
                        Button(self, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportO2).place(height=75, width=450, x=75, y=277)
                    else:
                        # This redirects to the exportBoth function so both can be used
                        Label(self, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=580, y=197)
                        Button(self, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportBoth).place(height=75, width=450, x=75, y=277)
                    top2.destroy()

                def cancelO2():
                    print("Cancelled.")
                    Button(self, text="Generate PDF", bg="Grey50", fg="White", font=("Century Gothic", 17, "bold"), state="disabled").place(height=75, width=450, x=75, y=277)
                    Label(self, text="Done!", font=('Century Gothic',10,'bold'), fg="Grey25", bg="Grey25").place(x=580, y=197)
                    top2.destroy()

                Button(top2, text="Cancel", fg="white", bg="IndianRed", font=('Century Gothic',17,'bold'), command=cancelO2).place(height=100, width=250, x=520, y=410)
                Button(top2, text="Confirm", fg= "white", bg="SpringGreen3", font=('Century Gothic',17,'bold'), command=confirmO2).place(height=100, width=250, x=780, y=410)
                Label(top2, text="Ensure that you selected the correct file by checking the file path, below:", fg="Orange", bg="Grey25", font=("Century Gothic",10, "bold"), justify="center").place(x=540, y=10)
                Label(top2, text=filepath2, fg="Grey85", bg="Grey25", width=66, justify="center", wraplength=500).place(x=540, y=30)
                Label(top2, text="Attach the O2 information file:", fg="White", bg="Grey25", font=("Century Gothic",20,"bold"), wraplength="300").place(x=555, y=180)
                Button(top2, text="Open", fg="white", bg="grey25", font=('Century Gothic',17,'bold'), command=o2info).place(width=170, height=75, x=820, y=175)
                Label(top2, text="Average:", fg="white",bg="grey25",font=SMALL_FONT).place(x=520,y=300)
                Label(top2, text=o2Meanvalue, fg="white",bg="grey15",font=SMALL_FONT).place(x=580,y=300, width=40)
                Label(top2, text="Maximum:", fg="white",bg="grey25",font=SMALL_FONT).place(x=520, y=320)
                Label(top2, text=o2Maxvalue, fg="white",bg="grey15",font=SMALL_FONT).place(x=580, y=320, width=40)
                Label(top2, text="Final:", fg="white",bg="grey25",font=SMALL_FONT).place(x=520, y=340)
                Label(top2, text=o2Finalvalue, fg="white",bg="grey15",font=SMALL_FONT).place(x=580, y=340, width=40)

            else:
                print("Nothing Selected.")

        # This prompts the user to select where the PDF is to be saved.
        def exportH2O():
                savepath = filedialog.asksaveasfilename(initialdir="/Desktop", title="Save the file", filetypes=(("PDF files","*.pdf"),("all files","*.*")))
                if savepath:
                    # This populates the data from the CSV file into the x1 and y1 variables
                    with open(filepath1) as csvfile:
                        csv.reader(csvfile, delimiter=',')
                    
                    h2o_pdfdata = [['Test Point ID:', str(hheaderlist[0]), 'Calibration Date:', str(hheaderlist[12])],
                    ['Client:', str(hheaderlist[1]), 'Specification:', str(hheaderlist[14])],
                    ['Instrument Serial#:', str(hheaderlist[11]), 'Instrument Flow:', str(hheaderlist[13])],
                    ['Test Gas:', str(hheaderlist[2]), 'Start Time:', str(hheaderlist[15])],
                    ['Technician:', str(hheaderlist[4]), 'Stop Time:', str(hheaderlist[16])],
                    ['Source Gas:', str(hheaderlist[3]), 'Stop Time:', str(hheaderlist[16])],
                    ['System Flow:', str(hheaderlist[5]), 'Maximum:', h2oMaxvalue],
                    ['Technicion:', str(hheaderlist[4]), 'Average:', h2oMeanvalue],
                    ['Comments:', str(hheaderlist[6]), 'Final:', h2oFinalvalue]
                    ]
                    pdf = FPDF()
                    pdf.set_font("Arial", size=10)
                    pdf.add_page()
                    pdf.image('h2opdfplt.png')
                    
                    col_width = pdf.w / 5.5
                    row_height = pdf.font_size*1.8
                    for row in h2o_pdfdata:
                        for item in row:
                            pdf.cell(col_width, row_height,
                                     txt=item, border=1)
                        pdf.ln(row_height)
                        
                    pdf.output(savepath)
                    
                    # This plots the data on a graph, using the matplotlib plt function
                    

                else:
                    print("Cancelled")

        def exportO2():
                savepath = filedialog.asksaveasfilename(initialdir="/Desktop", title="Save the file", filetypes=(("PDF files","*.pdf"),("all files","*.*")))
                if savepath:
                    # This populates the data from the CSV file into the x2 and y2 variables
                    with open(filepath2) as csvfile:
                        csv.reader(csvfile, delimiter=',')
                    
                    o2_pdfdata = [['Test Point ID:', str(oheaderlist[0]), 'Calibration Date:', str(oheaderlist[8])],
                    ['Client:', str(oheaderlist[1]), 'Specification:', str(oheaderlist[10])],
                    ['Instrument Serial Number:', str(oheaderlist[7]), 'Instrument Flow:', str(oheaderlist[9])],
                    ['Test Gas:', str(oheaderlist[2]), 'Start Time:', str(oheaderlist[15])],
                    ['Source Gas:', str(oheaderlist[3]), 'Stop Time:', str(oheaderlist[16])],
                    ['System Flow:', str(oheaderlist[5]), 'Maximum:', o2Maxvalue],
                    ['Technicion:', str(oheaderlist[4]), 'Average:', o2Meanvalue],
                    ['Comments:', str(oheaderlist[6]), 'Final:', o2Finalvalue]
                    ]
                    print(o2_pdfdata)
                    pdf = FPDF()
                    pdf.set_font("Arial", size=10)
                    pdf.add_page()
                    pdf.image('o2pdfplt.png')
                    
                    col_width = pdf.w / 5.5
                    row_height = pdf.font_size*1.8
                    for row in o2_pdfdata:
                        for item in row:
                            pdf.cell(col_width, row_height,
                                     txt=item, border=1)
                        pdf.ln(row_height)
                        
                    pdf.output(savepath)
                else:
                    print("Cancelled")

        def exportBoth():
                savepath = filedialog.asksaveasfilename(initialdir="/Desktop", title="Save the file", filetypes=(("PDF files","*.pdf"),("all files","*.*")))
                if savepath:
                    # This populates the data from the CSV file into the x1 and y1 variables
                    with open(filepath1) as csvfile:
                        csv.reader(csvfile, delimiter=',')

                    # This populates the data from the CSV file into the x2 and y2 variables
                    with open(filepath2) as csvfile:
                        csv.reader(csvfile, delimiter=',')
                    
                    # This plots the data on a graph, using the matplotlib plt function
                    o2_pdfdata = [['Test Point ID:', str(oheaderlist[0]), 'Calibration Date:', str(oheaderlist[8])],
                    ['Client:', str(oheaderlist[1]), 'Specification:', str(oheaderlist[10])],
                    ['Instrument Serial Number:', str(oheaderlist[7]), 'Instrument Flow:', str(oheaderlist[9])],
                    ['Test Gas:', str(oheaderlist[2]), 'Start Time:', str(oheaderlist[15])],
                    ['Source Gas:', str(oheaderlist[3]), 'Stop Time:', str(oheaderlist[16])],
                    ['System Flow:', str(oheaderlist[5]), 'Maximum:', o2Maxvalue],
                    ['Technicion:', str(oheaderlist[4]), 'Average:', o2Meanvalue],
                    ['Comments:', str(oheaderlist[6]), 'Final:', o2Finalvalue]
                    ]
                    print(o2_pdfdata)
                    pdf = FPDF()
                    pdf.set_font("Arial",size=16)
                    pdf.add_page()
                    pdf.cell(45)
                    pdf.cell(20,10,'Delta F Oxygen Analyzer',1,1,'C')
                    pdf.image('o2pdfplt.png')
                    
                    
                    pdf.set_font("Arial",size=10)
                    col_width = pdf.w / 5.5
                    row_height = pdf.font_size*1.8
                    for row in o2_pdfdata:
                        for item in row:
                            pdf.cell(col_width, row_height,
                                     txt=item, border=1)
                        pdf.ln(row_height)
                    
                    
                    h2o_pdfdata = [['Test Point ID:', str(hheaderlist[0]), 'Calibration Date:', str(hheaderlist[12])],
                    ['Client:', str(hheaderlist[1]), 'Specification:', str(hheaderlist[14])],
                    ['Instrument Serial#:', str(hheaderlist[11]), 'Instrument Flow:', str(hheaderlist[13])],
                    ['Test Gas:', str(hheaderlist[2]), 'Start Time:', str(hheaderlist[15])],
                    ['Technician:', str(hheaderlist[4]), 'Stop Time:', str(hheaderlist[16])],
                    ['Source Gas:', str(hheaderlist[3]), 'Stop Time:', str(hheaderlist[16])],
                    ['System Flow:', str(hheaderlist[5]), 'Maximum:', h2oMaxvalue],
                    ['Technicion:', str(hheaderlist[4]), 'Average:', h2oMeanvalue],
                    ['Comments:', str(hheaderlist[6]), 'Final:', h2oFinalvalue]
                    ]
                    pdf.set_font("Arial", size=10)
                    pdf.add_page()
                    pdf.image('h2opdfplt.png')
                    
                    col_width = pdf.w / 5.5
                    row_height = pdf.font_size*1.8
                    for row in h2o_pdfdata:
                        for item in row:
                            pdf.cell(col_width, row_height,
                                     txt=item, border=1)
                        pdf.ln(row_height)
                        
                    pdf.output(savepath)
                    
                    
                    
                else:
                    print("Cancelled")
        
        
        
        
        
        



        
app = RPiReader()

ani2 = animation.FuncAnimation(f2, PageOne.animateh2o, interval=1000)
ani1 = animation.FuncAnimation(f1, PageOne.animateo2, interval=1000)

app.mainloop()
