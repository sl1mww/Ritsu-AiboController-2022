import json
import sys
import time
from typing import DefaultDict
import urllib.request
import keyboard
from curses import BUTTON2_CLICKED
from tkinter import *
from tkinter.font import Font
from inputs import get_gamepad
import math
import threading

headers = {
'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExMSJ9.eyJzdWIiOiJlN\
jkyOWJjYy05NDg1LTRlNjItYWVhYy1jZGYzMDFiMjg3OTMiLCJleHAiOjE2NTgyMTQwNDIsImlz\
cyI6Imh0dHBzOi8vcHVibGljLmFwaS5haWJvLmNvbSIsImF1ZCI6IjQ1LjU0NzA2MTA2NzUyMDg\
xOTIiLCJqdGkiOiJhNDA2YmRjMS02Y2JlLTRmM2ItYWMyMC00NzZhMWQ0M2E3MmMiLCJpYXQiOj\
E2NTA0MzgwNDJ9.Fam_ltjdrPgRrUEpuHD6tjUL7AxbcgDhkxLJru_rhmbhrg02hwVG2gizpucv\
BbcX6GjT8yeLF5gZFrihLCWP3W-7aNUWT_Nlwv96_UuXaedfDelfeW77M23pbo1K_GJgeUifs0O\
zaPS83Hinu8gVgZL3f2oM5DjaAdwL4AqcFjxPmnfn-05OLO53k8-ui-qdh1vfBBWesfVHbsy2I9\
LMTGxtanEnJAIyHNFwKUco5WlNp5Y1aSnZVdoe9RStvmDSI-XLXUrRl1UTwt40XXns5NGPtX4xs\
n_UXmMKQCjPXIgLIMEENHbpXe1hvfYRs8W58nP_wlA2weHUE2rQyqEEAQ',
}
BASE_PATH = 'https://public.api.aibo.com/v1'
DEVICE_ID = "010ed9e5-bc49-40f7-9e42-e7e2d229e305"
TIME_OUT_LIMIT = 5

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    exit_event=threading.Event()

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        global dead 
        dead=False

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
       # self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor_controller(self):
        while (not dead):
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state
            if event.code == 'ABS_Y':
                if self.LeftJoystickY > 0.5:
                    move_forward()
                elif self.LeftJoystickY < -0.5:
                    move_backwards()
            if event.code == 'ABS_X':
                if self.LeftJoystickX > 0.5:
                    move_right()
                elif self.LeftJoystickX < -0.5:
                    move_left()
            if event.code == 'ABS_RX' and 'ABS_RY':
                if self.RightJoystickX > 0 and self.RightJoystickY > 0 : #for 0-90
                    turn_around2(self.RightJoystickX,self.RightJoystickY)
                if self.RightJoystickX > 0 and self.RightJoystickY < 0 :
                    turn_around3(self.RightJoystickX,self.RightJoystickY)
            if event.code == 'BTN_EAST':
                if self.B == 1:
                    bark()
            if event.code == 'BTN_NORTH':
                if self.Y == 1:
                    pee()
            if event.code == 'BTN_SELECT':
                if self.Back == 1:
                    set_mode()
            if event.code == 'BTN_START':
                if self.Start == 1:
                    convert2()
                    set_controller(0)

def turn_around2(x,y): #for 0-90
    
    angle = math.degrees(math.atan(x/y))
    angle = round(angle)
    
    print("turn around anticlockwise: "+str(angle)+"°")
    
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)      

def turn_around3(x,y): #for 90-180
    y = abs(y)
    angle = math.degrees(math.atan(y/x))
    angle = 90+round(angle)

    print("turn around anticlockwise: "+str(angle)+"°")
    
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)      

    
            

def move_forward():
    print("move forward")
    api_name="move_forward"
    data = '{"arguments":' '{"WalkSpeed":1,"WalkDistance":0.5}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def move_backwards():
    print("move backwards")
    api_name="move_forward"
    data = '{"arguments":' '{"WalkSpeed":1,"WalkDistance":-0.5}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def move_left():
    print("move to left")
    api_name="move_sideways"
    data = '{"arguments":' '{"WalkSpeed":2,"WalkDistance":0.5}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def move_right():
    print("move to right")
    api_name="move_sideways"
    data = '{"arguments":' '{"WalkSpeed":2,"WalkDistance":-0.5}''}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def turn_around():
    angle=scale.get() #get most recent angle

    if angle==0:
        angle=180

    if angle>=0:
        print("turn around anticlockwise: "+str(angle)+"°")
    else:
        print("turn around clockwise: "+str(angle)+"°")

    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def bark():
    print("bark")
    api_name="play_motion"

    data = '{"arguments":{"Category":"bark","Mode":"NONE"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def pee():
    print("pee")
    api_name="play_motion"

    data = '{"arguments":{"Category":"marking","Mode":"GIRL"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

data=''
def convert():
    if(button_mode['state']==DISABLED):
        button_mode["state"] = NORMAL
        button_switch["text"]="OFF"
        data='{"arguments":{"ModeName":"DEVELOPMENT"}}'
        return data
    elif (button_mode['state']==NORMAL):
        button_mode["state"]=DISABLED
        button_switch["text"]="ON"
        data='{"arguments":{"ModeName":"NORMAL"}}'
        return data

def set_mode():
    print("Setting mode...")

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/set_mode' + '/execute '
    req = urllib.request.Request(post_url, convert().encode(),headers=headers, method='POST')

    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
    executionId = post_result["executionId"]
    
    get_result_url = BASE_PATH + '/executions/' + executionId
    TimeOut = 0
    while True:
        req = urllib.request.Request(get_result_url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as res:
            response = res.read()
        get_result = json.loads(response)
        get_status = get_result["status"]

        if get_status == "SUCCEEDED":
            print(get_result)
            break
        elif get_status == "FAILED":
            print(get_result)
            break

        TimeOut += 1
        if TimeOut > TIME_OUT_LIMIT:
            print("Time out")
            break

        time.sleep(1)

def convert2():
    if(button_controller['state']==DISABLED):
        button_controller["state"] = NORMAL
        button_switch2["text"]="OFF"
        print("Controller mode enabled")
        set_controller(1)
    elif (button_controller['state']==NORMAL):
        button_controller["state"]=DISABLED
        button_switch2["text"]="ON"
        print("Controller mode disabled")
        set_controller(0)

def set_controller(state):
    global dead
    if state==1: #controller on
        joy = XboxController()

        #disabling all gui buttons
        for x in (button_w, button_s, button_a,button_d,button_b,button_p,button_mode):
            x.config(state = 'disabled')

        #disabling the keyboard
        root.unbind('w')
        root.unbind('s')
        root.unbind('a')
        root.unbind('d')
        root.unbind('b')
        root.unbind('p')
        scale.unbind("<ButtonRelease-1>")
          
    elif state==0: #controller off
        dead=True 

        #enabling all gui buttons
        for x in (button_w, button_s, button_a,button_d,button_b,button_p,button_mode):
            x.config(state = 'normal')
        
        #enabling the keyboard
        root.bind('w', lambda event: move_forward())
        root.bind('s', lambda event: move_backwards())
        root.bind('a', lambda event: move_left())
        root.bind('d', lambda event: move_right())
        root.bind('b', lambda event: bark())
        root.bind('p', lambda event: pee())
        scale.bind("<ButtonRelease-1>",lambda event: turn_around())


root =Tk()
root.title("Aibo controller")
root.geometry("1000x1000")

#virtual control buttons
button_w = Button(root, text="W", padx=30, pady=20, command=move_forward)
button_s = Button(root, text="S", padx=30, pady=20, command=move_backwards)
button_a = Button(root, text="A", padx=30, pady=20, command=move_left)
button_d = Button(root, text="D", padx=30, pady=20, command=move_right)
button_b = Button(root, text="Bark", padx=30, pady=20, command=bark,width=1,height=1)
button_p = Button(root, text="Pee", padx=30, pady=20, command=pee,width=1,height=1)
button_switch = Button(root, text="Mode", padx=10, pady=10)
#mode display
button_mode=Button(root,text="Developer Mode",state=DISABLED)
button_mode.config(height=1,width=10)
button_controller=Button(root,text="Controller",state=DISABLED)
button_controller.config(height=1,width=10)
#switch button
button_switch = Button(root, text="On", padx=10, pady=10, command=set_mode)
#button_switch2 = Button(root, text="On", padx=10, pady=10, command=lambda:[set_controller(), convert2()])
button_switch2 = Button(root, text="On", padx=10, pady=10, command= convert2)

#slider 
scale=Scale(root,from_=-180,to=180,orient="vertical")

#keyboards
root.bind('w', lambda event: move_forward())
root.bind('s', lambda event: move_backwards())
root.bind('a', lambda event: move_left())
root.bind('d', lambda event: move_right())
root.bind('b', lambda event: bark())
root.bind('p', lambda event: pee())
scale.bind("<ButtonRelease-1>",lambda event: turn_around())

#Position of buttons
button_w.grid(row=2, column=2)
button_s.grid(row=3, column=2)
button_a.grid(row=3, column=1)
button_d.grid(row=3, column=3)
button_mode.grid(row=4,column=1)
button_switch.grid(row=4,column=2)
button_controller.grid(row=4,column=3)
button_switch2.grid(row=4,column=4)
button_b.grid(row=3, column=4)
button_p.grid(row=2, column=4)
scale.grid(row=3,column=5)

#turn round text
f = Font(family='Helvetica', size=12)
v1 = StringVar()
txt = Text(root, height=0.5, width=10)
txt.configure(font=f)
txt.insert(0.5,"Turn around")
txt.grid(row=4, column=5)

root.mainloop()  

if __name__ == '__main__':
    exit(0)     