from tkinter import *
import serial
import serial.tools.list_ports
import time
from PIL import ImageTk, Image
import math
import threading

counter_row = 1
counter_cmd = 9
num = 0
loop = 0
goc_r1_1 = ""
goc_p2_1 = ""
goc_r3_1 = ""
goc_r4_1 = ""
goc_r1_2 = ""
goc_p2_2 = ""
goc_r3_2 = ""
goc_r4_2 = ""
start = 1
last_z = 0
last_r1 = 0
last_p2 = 0
last_r3 = 0
last_r4 = 0

class RobotControl(Frame):

    def __init__(self, parent=None, **options):

        Frame.__init__(self, parent, background='white')

        self.arduino = None
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
        ]
        if not arduino_ports:
            arduino_ports = ['COM Unknown']

        lf0 = LabelFrame(self, bg='orange', relief=FLAT)

        Label(lf0, text='Port:', bg='orange').grid(row=0, column=0, sticky=W, padx=5, pady=10)
        self.com = StringVar()
        self.com.set(arduino_ports[0])
        w = OptionMenu(lf0, self.com, arduino_ports)
        w.grid(row=0, column=1)



        Label(lf0, text='', bg='orange').grid(row=0, column=3, sticky=W, padx=10)

        Label(lf0, text='Baud rate:', bg='orange').grid(row=0, column=4, sticky=W)
        self.Baudrate = StringVar()
        self.Baudrate.set('115200')
        w1 = OptionMenu(lf0, self.Baudrate, '115200', '250000', '9600', '19600')
        w1.grid(row=0, column=5, padx=5)

        Label(lf0, text='', bg='orange').grid(row=0, column=6, sticky=W, padx=10)

        self.disconnect_btn = ImageTk.PhotoImage(Image.open("button_dis.png"))
        self.connect_btn = ImageTk.PhotoImage(Image.open('button_con.png'))
        self.home_btn = ImageTk.PhotoImage(Image.open('home.png'))

        self.btnConnect = Button(lf0, image=self.connect_btn, command=self.onConnect, borderwidth=0, activebackground='orange', bg='orange')
        self.btnConnect.grid(columnspan=2, row=0, column=7)
        Label(lf0, text='', bg='orange').grid(row=0, column=9, sticky=W, padx=390)
        self.btnHome = Button(lf0, image=self.home_btn, command=self.home_cmd, borderwidth=0, activebackground='orange', bg='orange')
        self.btnHome.grid(columnspan=2, row=0, column=10, padx=0)

        self.lable_status = Label(lf0, bg='orange')
        self.lable_status.grid(row=0, column=12)

        lf1 = LabelFrame(self, padx=200, pady=50, relief=FLAT, bg='white')

        Label(lf1, text='X', font=('monterrat', 20), bg='white').grid(row=0, column=1, padx=35)
        self.x = StringVar()
        self.x.set('0.0')
        Label(lf1, textvariable=self.x, fg='green', font=('monterrat', 20), bg='white').grid(row=0, column=2)

        Label(lf1, bg='white').grid(row=0, column=3, padx=35)

        Label(lf1, text='Y', font=('monterrat', 20), bg='white').grid(row=0, column=4, padx=35)
        self.y = StringVar()
        self.y.set('0.0')
        Label(lf1, textvariable=self.y, fg='green', font=('monterrat', 20), bg='white').grid(row=0, column=5)

        Label(lf1, bg='white').grid(row=0, column=6, padx=35)

        Label(lf1, text='Z', font=('monterrat', 20), bg='white').grid(row=0, column=7, padx=35)
        self.z = StringVar()
        self.z.set('0.0')
        Label(lf1, textvariable=self.z, fg='green', font=('monterrat', 20), bg='white').grid(row=0, column=8)

        Label(lf1, bg='white').grid(row=0, column=9, padx=35)

        Label(lf1, text='T', font=('monterrat', 20), bg='white').grid(row=0, column=10, padx=35)
        self.t = StringVar()
        self.t.set('0.0')
        Label(lf1, textvariable=self.t, fg='green', font=('monterrat', 20), bg='white').grid(row=0, column=11)

        Label(lf1, text='R1', font=('monterrat', 20), bg='white').grid(row=1, column=1, padx=35)
        self.j1 = StringVar()
        self.j1.set('0.0')
        Label(lf1, textvariable=self.j1, fg='blue', font=('monterrat', 20), bg='white').grid(row=1, column=2)

        Label(lf1, bg='white').grid(row=0, column=3, padx=35)

        Label(lf1, text='P2', font=('monterrat', 20), bg='white').grid(row=1, column=4, padx=35)
        self.j2 = StringVar()
        self.j2.set('0.0')
        Label(lf1, textvariable=self.j2, fg='blue', font=('monterrat', 20), bg='white').grid(row=1, column=5)

        Label(lf1, bg='white').grid(row=0, column=6, padx=35)

        Label(lf1, text='R3', font=('monterrat', 20), bg='white').grid(row=1, column=7, padx=35)
        self.j3 = StringVar()
        self.j3.set('0.0')
        Label(lf1, textvariable=self.j3, fg='blue', font=('monterrat', 20), bg='white').grid(row=1, column=8)

        Label(lf1, bg='white').grid(row=0, column=9, padx=35)

        Label(lf1, text='R4', font=('monterrat', 20), bg='white').grid(row=1, column=10, padx=35)
        self.j4 = StringVar()
        self.j4.set('0.0')
        Label(lf1, textvariable=self.j4, fg='blue', font=('monterrat', 20), bg='white').grid(row=1, column=11)

        self.image_mov = ImageTk.PhotoImage(Image.open('button_mov.png'))
        self.image_up = ImageTk.PhotoImage(Image.open('up.png'))
        self.image_down = ImageTk.PhotoImage(Image.open('down.png'))
        self.image_left = ImageTk.PhotoImage(Image.open('left.png'))
        self.image_right = ImageTk.PhotoImage(Image.open('right.png'))
        self.image_on = ImageTk.PhotoImage(Image.open('on.png'))
        self.image_off = ImageTk.PhotoImage(Image.open('off.png'))
        self.button_get = ImageTk.PhotoImage(Image.open('button_get.png'))
        self.button_start = ImageTk.PhotoImage(Image.open('button_start.png'))

        lf5 = LabelFrame(self, text='Tay gắp', padx=20, pady=20, bg='white', relief=FLAT)

        self.l51 = Label(lf5, text='Hand', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l51.grid(row=2, column=0, sticky=W)
        self.btnon = Button(lf5, text='', command=self.on, image=self.image_on, borderwidth=0, bg='white', activebackground='white')
        self.btnon.grid(row=2, column=2, padx=25, pady=0)
        self.btnoff = Button(lf5, text='', command=self.off, image=self.image_off, borderwidth=0, bg='white', activebackground='white')
        self.btnoff.grid(row=2, column=3, padx=0, pady=0)

        lf3 = LabelFrame(self, text='Động học thuận', padx=20, pady=20, bg='white', relief = FLAT)

        self.l31 = Label(lf3, text='R1:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l31.grid(row=2, column=0, sticky=W)
        self.r1 = StringVar()
        e31 = Entry(lf3, textvariable=self.r1, width=30)
        e31.grid(row=2, column=1)

        self.l32 = Label(lf3, text='P2:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l32.grid(row=3, column=0, sticky=W)
        self.p2 = StringVar()
        e32 = Entry(lf3, textvariable=self.p2, width=30)
        e32.grid(row=3, column=1)

        self.l33 = Label(lf3, text='R3:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l33.grid(row=4, column=0, sticky=W)
        self.r3 = StringVar()
        e33 = Entry(lf3, textvariable=self.r3, width=30)
        e33.grid(row=4, column=1)

        self.l33 = Label(lf3, text='R4:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l33.grid(row=5, column=0, sticky=W)
        self.r4 = StringVar()
        e33 = Entry(lf3, textvariable=self.r4, width=30)
        e33.grid(row=5, column=1)

######################## Arrows

        self.l41 = Label(lf3, text='Bước', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l41.grid(row=0, column=2, sticky=W)
        e41 = Spinbox(lf3, from_=1, to=100)
        e41.grid(row=0, column=3, columnspan=2)

        self.btnleft = Button(lf3, text='', image=self.image_left, borderwidth=0, bg='white', activebackground='white')
        self.btnleft.grid(row=2, column=2, padx=15, pady=0)
        Label(lf3, text='R1', font=('monterrat', 10), bg='white').grid(row=2, column=3, padx=0, pady=0)
        self.btnright = Button(lf3, text='', image=self.image_right, borderwidth=0, bg='white', activebackground='white')
        self.btnright.grid(row=2, column=4, padx=15, pady=0)

        self.btnleft = Button(lf3, text='', image=self.image_left, borderwidth=0, bg='white', activebackground='white')
        self.btnleft.grid(row=3, column=2, padx=0, pady=0)
        Label(lf3, text='P2', font=('monterrat', 10), bg='white').grid(row=3, column=3, padx=0, pady=0)
        self.btnright = Button(lf3, text='', image=self.image_right, borderwidth=0, bg='white', activebackground='white')
        self.btnright.grid(row=3, column=4, padx=0, pady=0)

        self.btnleft = Button(lf3, text='', image=self.image_left, borderwidth=0, bg='white', activebackground='white')
        self.btnleft.grid(row=4, column=2, padx=10, pady=0)
        Label(lf3, text='R3', font=('monterrat', 10), bg='white').grid(row=4, column=3, padx=25, pady=0)
        self.btnright = Button(lf3, text='', image=self.image_right, borderwidth=0, bg='white', activebackground='white')
        self.btnright.grid(row=4, column=4, padx=10, pady=0)

        self.btnleft = Button(lf3, text='', image=self.image_left, borderwidth=0, bg='white', activebackground='white')
        self.btnleft.grid(row=5, column=2, padx=10, pady=0)
        Label(lf3, text='R4', font=('monterrat', 10), bg='white').grid(row=5, column=3, padx=25, pady=0)
        self.btnright = Button(lf3, text='', image=self.image_right, borderwidth=0, bg='white', activebackground='white')
        self.btnright.grid(row=5, column=4, padx=10, pady=0)

####################

        self.btnmove = Button(lf3, text='MOVE', command=self.move_th, image=self.image_mov, borderwidth=0, bg='white', activebackground='white')
        self.btnmove.grid(row=6, column=1)

#################################################################################################

        lf4 = LabelFrame(self, text='Động học nghịch', padx=20, pady=20, bg='white', relief=FLAT)

        self.l45 = Label(lf4, text='Bước', font=('monterrat', 10), bg='white')
        self.l45.grid(row=1, column=2, sticky=S)
        e45 = Spinbox(lf4, from_=1, to=100)
        e45.grid(row=1, column=3, columnspan=2)

        self.l41 = Label(lf4, text='X:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l41.grid(row=2, column=0, sticky=W)
        self.dataX = StringVar()
        e41 = Entry(lf4, textvariable=self.dataX, width=30)
        e41.grid(row=2, column=1)

        self.l42 = Label(lf4, text='Y:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l42.grid(row=3, column=0, sticky=W)
        self.dataY = StringVar()
        e42 = Entry(lf4, textvariable=self.dataY, width=30)
        e42.grid(row=3, column=1)

        self.l43 = Label(lf4, text='Z:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l43.grid(row=4, column=0, sticky=W)
        self.dataZ = StringVar()
        e43 = Entry(lf4, textvariable=self.dataZ, width=30)
        e43.grid(row=4, column=1)

        self.l44 = Label(lf4, text='T:', font=('monterrat', 15), padx=3, pady=3, bg='white')
        self.l44.grid(row=5, column=0, sticky=W)
        self.dataT = StringVar()
        e44 = Entry(lf4, textvariable=self.dataT, width=30)
        e44.grid(row=5, column=1)

        self.btnmove = Button(lf4, text='MOVE', command=self.move_ng, image=self.image_mov, borderwidth=0, bg='white', activebackground='white')
        self.btnmove.grid(row=6, column=1)

        ############# Arrows

        self.btnup = Button(lf4, text='', image=self.image_up, borderwidth=0, bg='white', activebackground='white')
        self.btnup.grid(row=2, column=2, padx=25, pady=0)
        Label(lf4, text='X', font=('monterrat', 10), bg='white').grid(row=3, column=2, padx=25, pady=0)
        self.btndown = Button(lf4, text='', image=self.image_down, borderwidth=0, bg='white', activebackground='white')
        self.btndown.grid(row=4, column=2, padx=25, pady=0)

        self.btnup = Button(lf4, text='', image=self.image_up, borderwidth=0, bg='white', activebackground='white')
        self.btnup.grid(row=2, column=3, padx=0, pady=0)
        Label(lf4, text='Y', font=('monterrat', 10), bg='white').grid(row=3, column=3, padx=0, pady=0)
        self.btndown = Button(lf4, text='', image=self.image_down, borderwidth=0, bg='white', activebackground='white')
        self.btndown.grid(row=4, column=3, padx=0, pady=0)

        self.btnup = Button(lf4, text='', image=self.image_up, borderwidth=0, bg='white', activebackground='white')
        self.btnup.grid(row=2, column=4, padx=25, pady=0)
        Label(lf4, text='Z', font=('monterrat', 10), bg='white').grid(row=3, column=4, padx=25, pady=0)
        self.btndown = Button(lf4, text='', image=self.image_down, borderwidth=0, bg='white', activebackground='white')
        self.btndown.grid(row=4, column=4, padx=25, pady=0)

        self.btnup = Button(lf4, text='', image=self.image_up, borderwidth=0, bg='white', activebackground='white')
        self.btnup.grid(row=2, column=5, padx=0, pady=0)
        Label(lf4, text='T', font=('monterrat', 10), bg='white').grid(row=3, column=5, padx=0, pady=0)
        self.btndown = Button(lf4, text='', image=self.image_down, borderwidth=0, bg='white', activebackground='white')
        self.btndown.grid(row=4, column=5, padx=0, pady=0)

###########################################

        lf6 = LabelFrame(self, text='Học lệnh', padx=20, pady=20, bg='white', width=1500, relief=FLAT)

        self.btnget1 = Button(lf6, text='get1', command=self.get1_cmd, image=self.button_get, borderwidth=0, bg='white', activebackground='white')
        self.btnget1.grid(row=4, column=1, pady=5)

        self.btnget2 = Button(lf6, text='get2', command=self.get2_cmd, image=self.button_get, borderwidth=0, bg='white', activebackground='white')
        self.btnget2.grid(row=4, column=4, pady=5)

        self.btnstart = Button(lf6, text='start', command=self.hoc_lenh, image=self.button_start, borderwidth=0, bg='white', activebackground='white')
        self.btnstart.grid(row=5, column=2, pady=5)

        self.l61 = Label(lf6, text='X1:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l61.grid(row=0, column=0, sticky=W)
        self.dataX1 = StringVar()
        e61 = Entry(lf6, textvariable=self.dataX1, width=15)
        e61.grid(row=0, column=1)

        self.l62 = Label(lf6, text='Y1:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l62.grid(row=1, column=0, sticky=W)
        self.dataY1 = StringVar()
        e62 = Entry(lf6, textvariable=self.dataY1, width=15)
        e62.grid(row=1, column=1)

        self.l63 = Label(lf6, text='Z1:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l63.grid(row=2, column=0, sticky=W)
        self.dataZ1 = StringVar()
        e63 = Entry(lf6, textvariable=self.dataZ1, width=15)
        e63.grid(row=2, column=1)

        self.l63 = Label(lf6, text='T1:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l63.grid(row=3, column=0, sticky=W)
        self.v63 = StringVar()
        e63 = Entry(lf6, textvariable=self.v63, width=15)
        e63.grid(row=3, column=1)

        self.l64 = Label(lf6, text='Số lần lặp', font=('monterrat', 7), padx=3, pady=3, bg='white')
        self.l64.grid(row=2, column=2, sticky=S, padx=20)
        self.number = StringVar()
        e64 = Entry(lf6, textvariable=self.number, width=7)
        e64.grid(row=3, column=2)

        self.l65 = Label(lf6, text='X2:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l65.grid(row=0, column=3, sticky=W)
        self.dataX2 = StringVar()
        e65 = Entry(lf6, textvariable=self.dataX2, width=15)
        e65.grid(row=0, column=4)

        self.l66 = Label(lf6, text='Y2:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l66.grid(row=1, column=3, sticky=W)
        self.dataY2 = StringVar()
        e66 = Entry(lf6, textvariable=self.dataY2, width=15)
        e66.grid(row=1, column=4)

        self.l67 = Label(lf6, text='Z2:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l67.grid(row=2, column=3, sticky=W)
        self.dataZ2 = StringVar()
        e67 = Entry(lf6, textvariable=self.dataZ2, width=15)
        e67.grid(row=2, column=4)

        self.l68 = Label(lf6, text='T2:', font=('monterrat', 10), padx=3, pady=3, bg='white')
        self.l68.grid(row=3, column=3, sticky=W)
        self.v68 = StringVar()
        e68 = Entry(lf6, textvariable=self.v68, width=15)
        e68.grid(row=3, column=4)

########################################

        lf7 = LabelFrame(self, text='Thông tin', padx=0, pady=0, bg='white', relief=FLAT)
        self.v7 = StringVar()
        self.v7.set('Hellllo')
        self.mess = Listbox(lf7, bg='black', fg='green', font=('monterrat', 10), width=50, height=9)
        self.mess.grid(row=0, column=0)

        lf8 = LabelFrame(self, text='G-Code', padx=0, pady=0, bg='white', relief=FLAT)
        gcode = Listbox(lf8, bg='lightblue', fg='black', font=('monterrat', 10), width=50, height=9)
        gcode.insert(1, 'G-Code hiển thị ở đây')
        gcode.grid(row=0, column=0, columnspan=4)
        text = Label(lf8, text='G-code:', bg='white')
        text.grid(row=1, column=0)
        self.v8 = StringVar()
        e8 = Entry(lf8, textvariable=self.v8, width=30)
        e8.grid(row=1, column=1)
        self.btnrun = Button(lf8, text='RUN', command=self.run_cmd, borderwidth=0, bg='lightgreen', activebackground='white')
        self.btnrun.grid(row=1, column=2)
        self.btnrun = Button(lf8, text='Clear', command=self.clear_cmd, borderwidth=0, bg='yellow', activebackground='white')
        self.btnrun.grid(row=1, column=3)

        ##################################


        #lf0.pack(side=TOP, fill=BOTH)
        #lf1.pack(side=TOP, fill=BOTH)


        #lf5.pack(side=RIGHT, fill=BOTH, expand=YES)
        #lf3.pack(side=RIGHT, fill=BOTH, expand=YES)

        #lf4.pack(side=TOP, fill=BOTH, expand=YES)
        #lf7.pack(side=RIGHT, fill=BOTH, expand=YES)
        #lf6.pack(side=TOP, fill=BOTH, expand=YES)

        ####################
        lf0.grid(row=0, columnspan=4)
        lf1.grid(row=1, columnspan=4)
        lf4.grid(row=2, column=0, stick='W')
        lf5.grid(row=2, column=2, stick='NW')
        lf3.grid(row=2, column=1, stick='W')

        lf6.grid(row=3, column=0, stick='W')
        lf7.grid(row=3, column=1, stick='NW')
        lf8.grid(row=3, column=2, stick='NW')


        # lf7.pack(side=TOP, fill=BOTH, expand=YES)

    def on(self):
        if self.arduino is not None and self.arduino.isOpen():
            x = 'on'
            self.arduino.write(x.encode('utf-8'))
            print(x)

    def off(self):
        if self.arduino is not None and self.arduino.isOpen():
            x = 'off'
            self.arduino.write(x.encode('utf-8'))
            print(x)

    def clear_cmd(self):
        print('Clear G-code')

    def run_cmd(self):
        print('RUN G-code')

    def home_cmd(self):
        self.x.set("366")
        if self.arduino is not None and self.arduino.isOpen():
            x = 'home'
            self.arduino.write(x.encode('utf-8'))
            print(x)

    def get1_cmd(self):
        print('get1')

    def get2_cmd(self):
        print('get2')

    def start_cmd(self):
        print('start')

    def move_th(self):

        global last_r1
        global last_p2
        global last_r3
        global last_r4
        a = last_r1
        b = last_p2
        c = last_r3
        d = last_r4

        a = last_r1
        b = last_p2
        c = last_r3
        d = last_r4
        if self.r1.get() != "":
            a = int(self.r1.get())
            last_r1 = a
        if self.p2.get() != "":
            b = int(self.p2.get())
            last_p2 = b
        if self.r3.get() != "":
            c = int(self.r3.get())
            last_r3 = c
        if self.r4.get() != "":
            d = int(self.r4.get())
            last_r4 = d

        self.z.set(b)
        self.t.set(d)

        self.j1.set(a)
        self.j2.set(b)
        self.j3.set(c)
        self.j4.set(d)

        la = 216
        lb = 150
        goc_r1 = a
        goc_r3 = c
        print(goc_r1)
        print(goc_r3)
        toadoX = la * math.cos(math.radians(goc_r1)) + lb * math.cos(math.radians(goc_r1+goc_r3))
        toadoY = la * math.sin(math.radians(goc_r1)) + lb * math.sin(math.radians(goc_r1+goc_r3))
        print(int(toadoX))
        print(int(toadoY))

        self.x.set(int(toadoX))
        self.y.set(int(toadoY))

        if self.arduino is not None and self.arduino.isOpen():
            x = 'a' + self.r1.get() + 'b' + self.p2.get() + 'c' + self.r3.get() + 'd' + self.r4.get()
            self.arduino.write(x.encode('utf-8'))
            print(x)

    def hoc_lenh(self):

        global goc_r1_1
        global goc_p2_1
        global goc_r3_1
        global goc_r4_1
        global goc_r1_2
        global goc_p2_2
        global goc_r3_2
        global goc_r4_2
        global num
        global start

        def dong_hoc_nghich(_x, _y):
            la = 216
            lb = 150

            x = int(_x)
            y = int(_y)

            l = math.sqrt(x * x + y * y)
            cos_alpha = (l * l + la * la - lb * lb) / (2 * l * la)
            alpha = math.degrees(math.acos(cos_alpha))
            goc_r1 = math.degrees(math.asin(y / l)) - alpha

            cos_beta = (la * la + lb * lb - x * x - y * y) / (2 * la * lb)
            beta = math.degrees(math.acos(cos_beta))
            goc_r3 = 180 - beta

            goc_r4 = goc_r1 + goc_r3
            return goc_r1, goc_r3, goc_r4

        goc_r1_1, goc_r3_1, goc_r4_1 = dong_hoc_nghich(self.dataX1.get(), self.dataY1.get())
        goc_r1_2, goc_r3_2, goc_r4_2 = dong_hoc_nghich(self.dataX2.get(), self.dataY2.get())

        if self.dataZ1.get() == "":
            goc_p2_1 = 0
        else:
            goc_p2_1 = self.dataZ1.get()

        if self.dataZ2.get() == "":
            goc_p2_2 = 0
        else:
            goc_p2_2 = self.dataZ2.get()

        num = int(self.number.get())
        start = 1
        self.cap_nhat()

    def cap_nhat(self):
        global counter_row
        global counter_cmd
        global loop
        global num
        global start
        thread = threading.Timer(1, self.cap_nhat)
        thread.start()
        self.read = StringVar()
        #print(num)
        if loop == (num+1): #1
            loop = 0
            counter_row = 1
            counter_cmd = 8
            thread.cancel()

        if self.arduino is not None and self.arduino.isOpen():

            if counter_cmd == 9:
                loop += 1
                counter_cmd = 1
                if loop < (num+1):
                    self.mess.insert(counter_row, "Đang chạy lần " + str(loop))
                    counter_row += 1

            if start == 1:
                self.read.set(self.arduino.read(self.arduino.inWaiting()))
                self.read.set("1")

            self.read.set(self.arduino.read(self.arduino.inWaiting()))
            print(self.read.get())

            if self.read.get() == 'b\'ok\'' or start == 1:
                if start == 1:
                    start = 0

                self.read.set("1")
                self.mess.insert(counter_row, "ok")
                counter_row += 1
                if counter_cmd == 1:
                    j = 'off'
                    self.arduino.write(j.encode('utf-8'))
                    print(j)

                if counter_cmd == 2 or counter_cmd == 5 or counter_cmd == 8:
                    x = 'a' + 'b0' + 'c' + 'd'
                    self.arduino.write(x.encode('utf-8'))
                    print(x)
                    self.j2.set("0")
                    self.z.set("0")

                if counter_cmd == 3:
                    y = 'a' + str(goc_r1_1) + 'b' + str(goc_p2_1) + 'c' + str(goc_r3_1) + 'd' + str(goc_r4_1)
                    self.arduino.write(y.encode('utf-8'))
                    print(y)
                    self.x.set(self.dataX1.get())
                    self.y.set(self.dataY1.get())
                    self.z.set(int(goc_p2_1))
                    self.t.set(int(goc_r4_1))

                    self.j1.set(int(goc_r1_1))
                    self.j2.set(int(goc_p2_1))
                    self.j3.set(int(goc_r3_1))
                    self.j4.set(int(goc_r4_1))


                if counter_cmd == 4:
                    k = 'on'
                    self.arduino.write(k.encode('utf-8'))
                    print(k)

                if counter_cmd == 6:
                    z = 'a' + str(goc_r1_2) + 'b' + str(goc_p2_2) + 'c' + str(goc_r3_2) + 'd' + str(goc_r4_2)
                    self.arduino.write(z.encode('utf-8'))
                    print(z)
                    self.x.set(self.dataX2.get())
                    self.y.set(self.dataY2.get())
                    self.z.set(int(goc_p2_2))
                    self.t.set(int(goc_r4_2))

                    self.j1.set(int(goc_r1_2))
                    self.j2.set(int(goc_p2_2))
                    self.j3.set(int(goc_r3_2))
                    self.j4.set(int(goc_r4_2))

                if counter_cmd == 7:
                    j = 'off'
                    self.arduino.write(j.encode('utf-8'))
                    print(j)

                counter_cmd += 1

    def move_ng(self):
        global last_z
        la = 216
        lb = 150

        x = int(self.dataX.get())
        y = int(self.dataY.get())

        l = math.sqrt(x * x + y * y)
        cos_alpha = (l * l + la * la - lb * lb) / (2 * l * la)
        alpha = math.degrees(math.acos(cos_alpha))
        goc_r1 = math.degrees(math.asin(y / l)) - alpha

        cos_beta = (la * la + lb * lb - x * x - y * y) / (2 * la * lb)
        beta = math.degrees(math.acos(cos_beta))
        goc_r3 = 180 - beta

        goc_r4 = goc_r1 + goc_r3

        if self.arduino is not None and self.arduino.isOpen():
            j = 'a' + str(goc_r1) + 'b' + self.dataZ.get() + 'c' + str(goc_r3) + 'd' + str(goc_r4)
            self.arduino.write(j.encode('utf-8'))
            print(j)

        z = last_z
        if self.dataZ.get() != "":
            z = int(self.dataZ.get())
            last_z = z
        self.x.set(x)
        self.y.set(y)
        self.z.set(str(z))
        self.t.set(int(goc_r4))

        self.j1.set(int(goc_r1))
        self.j2.set(str(z))
        self.j3.set(int(goc_r3))
        self.j4.set(int(goc_r4))

    def onConnect(self):
        if self.arduino is None or not self.arduino.isOpen():
            self.connect_arduino()
            self.btnConnect.config(image=self.disconnect_btn)

            if self.arduino is not None and self.arduino.is_open:
                self.arduino.write(bytes('M17\r', 'utf-8'))

        else:
            if self.arduino is not None and self.arduino.isOpen():
                self.arduino.write(bytes('M18\r', 'utf-8'))
            self.disconnect_arduino()
            self.btnConnect.config(image=self.connect_btn)

    def connect_arduino(self):
        print('Connecting...')
        self.arduino = serial.Serial(self.com.get(), self.Baudrate.get())
        time.sleep(3)
        print('Connection established successfully')

    def disconnect_arduino(self):
        if self.arduino.isOpen():
            print('Disconnecting...')
            self.arduino.close()
            time.sleep(3)
            print('Disconnection established successfully')

if __name__ == '__main__':
    window = Tk()
    #window.state('zoomed')
    window.wm_title("SCARA ROBOT GUI")
    window.iconbitmap('icon_gui.ico')
    RobotControl(window).grid()
    window.mainloop()








