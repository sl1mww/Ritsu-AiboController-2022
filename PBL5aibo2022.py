import json
import time
from typing import DefaultDict
import urllib.request
from curses import BUTTON2_CLICKED
from tkinter import *
from tkinter.font import Font
from inputs import get_gamepad
import math
import threading



headers = {
'Authorization': 'Bearer ', # insert access token after "Bearer " 
} 
BASE_PATH = 'https://public.api.aibo.com/v1' 
DEVICE_ID = "" #input device ID for particular aibo
TIME_OUT_LIMIT = 5 #time limit for changing from developer-normal (vice-versa)

root =Tk() 
root.title("Aibo controller")
root.geometry("800x350") #GUI size
latestcommand = StringVar() #elevation text
latestcommand2= StringVar() #azimuth text

class XboxController(object): #class for xbox360 controller
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
        self.DPadX = 0
        self.DPadY = 0

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
                elif event.code == 'ABS_HAT0X':
                    self.DPadX = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.DPadY = event.state
            if event.code == 'ABS_Y':
                if self.LeftJoystickY > 0.5:#mapping left joystick Y axis
                    move_forward()
                elif self.LeftJoystickY < -0.5: #mapping left joystick y axis
                    move_backwards()
            if event.code == 'ABS_X':  
                if self.LeftJoystickX > 0.5: #mapping left joystick X axis 
                    move_right()
                elif self.LeftJoystickX < -0.5: #mapping left joystick X axis
                    move_left()
            if event.code == 'ABS_RX' and 'ABS_RY': #mapping right joystick X & Y axis
                if self.RightJoystickX > 0 and self.RightJoystickY > 0 : #for 0-90
                    turn_around2(self.RightJoystickX,self.RightJoystickY)
                if self.RightJoystickX > 0 and self.RightJoystickY < 0 : #for 90-180
                    turn_around3(self.RightJoystickX,self.RightJoystickY)
                if self.RightJoystickX < 0 and self.RightJoystickY > 0 : #for -(0-90)
                    turn_around4(self.RightJoystickX,self.RightJoystickY)
                if self.RightJoystickX < 0 and self.RightJoystickY < 0 : #for 90-180
                    turn_around5(self.RightJoystickX,self.RightJoystickY) 
            #mapping buttons 
            if event.code == 'ABS_HAT0Y': 
                if self.DPadY == -1:
                    look_up()
                elif self.DPadY == 1:
                    look_down()
            if event.code == 'ABS_HAT0X':
                if self.DPadX == 1:
                    look_right()
                elif self.DPadX == -1:
                    look_left()
            if event.code == 'BTN_EAST': 
                if self.B:
                    bark()
            if event.code == 'BTN_NORTH':
                if self.Y:
                    stand_straight()
            if event.code == 'BTN_START':
                if self.Start:
                    set_mode()
            if event.code == 'BTN_SELECT':
                if self.Back:
                    convert2()
            if event.code == 'BTN_THUMBL':
                if self.LeftThumb:
                    reset_head()
            if event.code == 'BTN_SOUTH':
                if self.A:
                    sit()
            if event.code == 'BTN_WEST':
                if self.X:
                    pee()
            if event.code == 'ABS_Z':
                if self.LeftTrigger:
                    dance()
            if event.code == 'ABS_RZ':
                if self.RightTrigger:
                    sneeze()
            if event.code == 'BTN_TL':
                if self.LeftBumper == 1:
                    jiggle()
            if event.code =='BTN_TR':
                if self.RightBumper == 1:
                    belch()

def turn_around2(x,y): #for 0-90
    angle = math.degrees(math.atan(x/y))
    angle = round(angle/10)*10 #round off to nearest 10
    
    print("turn around anticlockwise: "+str(angle)+"°")
    latestcommand.set("Turn around anticlockwise: "+str(angle)+"°")
    
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
    angle = 90+round(angle/10)*10 #round off to nearest 10

    print("turn around anticlockwise: "+str(angle)+"°")
    latestcommand.set("Turn around anticlockwise: "+str(angle)+"°")

    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)   

def turn_around4(x,y): #for -0--90
    y = abs(y)
    angle = math.degrees(math.atan(x/y))
    angle = round(angle/10)*10 #round off to nearest 10
    print("turn around clockwise: "+str(angle)+"°")
    latestcommand.set("Turn around clockwise: "+str(angle)+"°")
    
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)  

def turn_around5(x,y): #for -90-180
    y = abs(y)
    angle = math.degrees(math.atan(y/x))
    angle = -90+round(angle/10)*10 #round off to nearest 10
    print("turn around clockwise: "+str(angle)+"°")
    latestcommand.set("Turn around clockwise: "+str(angle)+"°")
    
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)    

def move_forward():

    print("move forward")
    latestcommand.set("Move Forwards")
    api_name="move_forward"
    data = '{"arguments":' '{"WalkSpeed":1,"WalkDistance":0.5}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def move_backwards():
    print("move backwards")
    latestcommand.set("Move Backwards")
    api_name="move_forward"
    data = '{"arguments":' '{"WalkSpeed":1,"WalkDistance":-0.5}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def move_left():
    print("move to left")
    latestcommand.set("Move to Left")
    api_name="move_sideways"
    data = '{"arguments":' '{"WalkSpeed":2,"WalkDistance":0.5}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def move_right():
    print("move to right")
    latestcommand.set("Move to Right")
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
        latestcommand.set("Turn around anticlockwise: "+str(angle)+"°")
        
    else:
        print("turn around clockwise: "+str(angle)+"°")
        latestcommand.set("Turn around clockwise: "+str(angle)+"°")

    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":' + str(angle)+'}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def bark():
    print("bark")
    latestcommand.set("Bark")
    api_name="play_motion"

    data = '{"arguments":{"Category":"bark","Mode":"NONE"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def pee():
    print("pee")
    latestcommand.set("Pee")
    api_name="play_motion"

    data = '{"arguments":{"Category":"marking","Mode":"GIRL"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

Xazimuth=0     #for keeping track of increment along X axis (azimuth)
Yelevation=0   #for keeping track of increment along Y axis (elevation)
def look_up():
    global Yelevation
    global Xazimuth
    
    #for incrementing and resetting to 0 once reach 40
    if Yelevation==40: 
        Yelevation=0
    else:
        Yelevation +=10

    print("look up")
    latestcommand.set("Look up. Current elevation="+str(Yelevation))
    latestcommand2.set("Current azimuth="+str(Xazimuth))

    api_name="move_head"
    data = '{"arguments":' '{"Azimuth":'+ str(Xazimuth)+',"Elevation":' + str(Yelevation) + ', "Velocity":50}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')

    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
def look_down():
    global Yelevation
    global Xazimuth

    if Yelevation==-40:
        Yelevation=0
    else:
        Yelevation -=10

    print("look down")
    latestcommand.set("Look down. Current elevation="+str(Yelevation))
    latestcommand2.set("Current azimuth="+str(Xazimuth))

    api_name="move_head"
    data = '{"arguments":' '{"Azimuth":'+ str(Xazimuth)+',"Elevation":' + str(Yelevation) + ', "Velocity":50}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')

    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
def look_right():
    global Yelevation
    global Xazimuth

    #for incrementing and resetting to 0 once reach 80
    if Xazimuth==-80:
        Xazimuth=0
    else:
        Xazimuth -=20

    print("look right")
    latestcommand.set("Look right. Current elevation="+str(Yelevation))
    latestcommand2.set("Current azimuth="+str(Xazimuth))

    api_name="move_head"
    data = '{"arguments":' '{"Azimuth":' + str(Xazimuth) + ',"Elevation":'+str(Yelevation)+', "Velocity":50}''}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
def look_left():
    global Yelevation
    global Xazimuth

    if Xazimuth==80:
        Xazimuth=0
    else:
        Xazimuth +=20

    print("look left")
    latestcommand.set("Look left. Current elevation="+str(Yelevation))
    latestcommand2.set("Current azimuth="+str(Xazimuth))

    api_name="move_head"
    data = '{"arguments":' '{"Azimuth":' + str(Xazimuth) + ',"Elevation":'+str(Yelevation)+', "Velocity":50}''}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
def reset_head():
    global Xazimuth, Yelevation

    Xazimuth=0
    Yelevation=0

    print("head reset")
    latestcommand.set("Head reset. Current elevation="+str(Yelevation))
    latestcommand2.set("Current azimuth="+str(Xazimuth))
    api_name="move_head"
    data = '{"arguments":' '{"Azimuth":' + str(Xazimuth) + ',"Elevation":'+str(Yelevation)+', "Velocity":50}''}'


    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')

    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def sit():
    print("sit")
    latestcommand.set("Sit")
    api_name="change_posture"

    data = '{"arguments":{"FinalPosture":"sit"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def stand_straight ():
    print("stand")
    latestcommand.set("Stand")
    api_name="change_posture"

    data = '{"arguments":{"FinalPosture":"sit_and_raise_both_hands"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def jiggle():
    print("jiggle")
    latestcommand.set("Jiggle")
    api_name="play_motion"

    data = '{"arguments":{"Category":"jiggle", "Mode":"NONE"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def dance():
    print("dance")
    latestcommand.set("Dance")
    api_name="play_motion"

    data = '{"arguments":{"Category":"dance", "Mode":"NONE"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def belch():
    print("belch")
    latestcommand.set("Belch")
    api_name="play_motion"

    data = '{"arguments":{"Category":"belch", "Mode":"NONE"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def sneeze():
    print("sneeze")
    latestcommand.set("Sneeze")
    api_name="play_motion"

    data = '{"arguments":{"Category":"sneeze", "Mode":"NONE"}}'

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)


data=''
def convert(): #for state of buttons "Developer Mode" and "OFF"
    if(button_mode['state']==DISABLED):
        button_mode["state"] = NORMAL
        button_switch["text"]="OFF" 
        data='{"arguments":{"ModeName":"DEVELOPMENT"}}' #set data as DEVELOPMENT 
        return data #data will be used in set_mode()
    elif (button_mode['state']==NORMAL):
        button_mode["state"]=DISABLED
        button_switch["text"]="ON"
        data='{"arguments":{"ModeName":"NORMAL"}}' #set data as NORMAL
        return data

def set_mode(): #for setting development/normal mode 
    print("Setting mode...")

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/set_mode' + '/execute '
    req = urllib.request.Request(post_url, convert().encode(),headers=headers, method='POST') #send out request of data (convert())

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

def convert2(): #for converting between Controller/GUI mode
    if(button_controller['state']==DISABLED):
        button_controller["state"] = NORMAL
        button_switch2["text"]="OFF"
        print("Controller mode enabled")
        latestcommand.set("Controller mode enabled")
        set_controller(1) #switch on 
    elif (button_controller['state']==NORMAL):
        button_controller["state"]=DISABLED
        button_switch2["text"]="ON"
        print("Controller mode disabled")
        latestcommand.set("Controller mode disabled")
        set_controller(0) #switch off 

def set_controller(state): #for setting controller/GUI mode 
    global dead 
    if state==1: #controller on, make class 
        joy = XboxController()

        #disabling all gui buttons
        for x in (button_w, button_s, button_a,button_d,button_b,button_p,
        button_mode,scale,button_up,button_down,button_right,button_left,
        button_headreset,button_sit,button_stand,button_jiggle,button_dance,button_belch,button_sneeze):
            x.config(state = 'disabled')

       #disabling (unbind) the keyboard
        root.unbind('w')
        root.unbind('s')
        root.unbind('a')
        root.unbind('d')
        root.unbind('b')
        root.unbind('p')
        root.unbind('<Up>')
        root.unbind('<Down>')
        root.unbind('<Right>')
        root.unbind('<Left>')
        root.unbind('<space>')
        root.unbind('z')
        root.unbind('x')
        root.unbind('c')
        root.unbind('v')
        root.unbind('b')
        root.unbind('n')
        scale.unbind("<ButtonRelease-1>")

    elif state==0: #controller off
        dead=True 

        #enabling all gui buttons
        for x in (button_w, button_s, button_a,button_d,button_b,button_p,
        button_mode,scale,button_up,button_down,button_right,button_left,
        button_headreset,button_sit,button_stand,button_jiggle,button_dance,button_belch,button_sneeze):
            x.config(state = 'normal')

        #enabling (bind) the keyboard
        root.bind('w', lambda event: move_forward())
        root.bind('s', lambda event: move_backwards())
        root.bind('a', lambda event: move_left())
        root.bind('d', lambda event: move_right())
        root.bind('b', lambda event: bark())
        root.bind('p', lambda event: pee())
        root.bind('<Up>', lambda event: look_up())
        root.bind('<Down>', lambda event: look_down())
        root.bind('<Right>', lambda event: look_right())
        root.bind('<space>', lambda event: reset_head())
        root.bind('<Left>', lambda event: look_left())
        root.bind('j', lambda event: sit())
        root.bind('u', lambda event: stand_straight())
        root.bind('z', lambda event: bark())
        root.bind('x', lambda event: pee())
        root.bind('c', lambda event: jiggle())
        root.bind('v', lambda event: dance())
        root.bind('b', lambda event: belch())
        root.bind('n', lambda event: sneeze())
        scale.bind("<ButtonRelease-1>",lambda event: turn_around())

#GUI virtual control buttons 
button_w = Button(root, text="W", padx=30, pady=20, command=move_forward)
button_s = Button(root, text="S", padx=30, pady=20, command=move_backwards)
button_a = Button(root, text="A", padx=30, pady=20, command=move_left)
button_d = Button(root, text="D", padx=30, pady=20, command=move_right)
button_b = Button(root, text="Bark", padx=30, pady=20, command=bark,width=1,height=1)
button_p = Button(root, text="Pee", padx=30, pady=20, command=pee,width=1,height=1)
button_up = Button(root, text="Look ⬆️", padx=30, pady=20, command=look_up,width=1,height=1)
button_down = Button(root, text="Look ⬇️", padx=30, pady=20, command=look_down, width=1,height=1)
button_right = Button(root, text="Look ➡️", padx=30, pady=20, command=look_right, width=1,height=1)
button_left = Button(root, text="Look ⬅️", padx=30, pady=20, command=look_left, width=1,height=1)
button_headreset = Button(root, text="Reset", padx=30, pady=20, command=reset_head, width=1,height=1)
button_sit = Button(root, text="Sit", padx=30, pady=20, command=sit, width=1,height=1)
button_stand = Button(root, text="Stand", padx=30, pady=20, command=stand_straight, width=1,height=1)
button_jiggle = Button(root, text="Jiggle", padx=30, pady=20, command=jiggle, width=1,height=1)
button_dance = Button(root, text="Dance", padx=30, pady=20, command=dance, width=1,height=1)
button_belch = Button(root, text="Belch", padx=30, pady=20, command=belch, width=1,height=1)
button_sneeze = Button(root, text="Sneeze", padx=30, pady=20, command=sneeze, width=1,height=1)

button_switch = Button(root, text="Mode", padx=10, pady=10)
#mode display
button_mode=Button(root,text="Developer Mode",state=DISABLED)
button_mode.config(height=1,width=10)
button_controller=Button(root,text="Controller",state=DISABLED)
button_controller.config(height=1,width=10)

#switch buttons
button_switch = Button(root, text="On", padx=10, pady=10, command=set_mode) #developer mode switch button
button_switch2 = Button(root, text="On", padx=10, pady=10, command= convert2) #controller mode switch button

#slider for turning round 
scale=Scale(root,from_=-180,to=180,orient="vertical")

#enabling (bind) buttons to keyboards
root.bind('w', lambda event: move_forward())
root.bind('s', lambda event: move_backwards())
root.bind('a', lambda event: move_left())
root.bind('d', lambda event: move_right())
root.bind('<Up>', lambda event: look_up())
root.bind('<Down>', lambda event: look_down())
root.bind('<Right>', lambda event: look_right())
root.bind('<Left>', lambda event: look_left())
root.bind('<space>', lambda event: reset_head())
root.bind('j', lambda event: sit())
root.bind('u', lambda event: stand_straight())
root.bind('z', lambda event: bark())
root.bind('x', lambda event: pee())
root.bind('c', lambda event: jiggle())
root.bind('v', lambda event: dance())
root.bind('b', lambda event: belch())
root.bind('n', lambda event: sneeze())
scale.bind("<ButtonRelease-1>",lambda event: turn_around())

#Position of buttons and other components on GUI
button_w.grid(row=2, column=2)
button_s.grid(row=3, column=2)
button_a.grid(row=3, column=1)
button_d.grid(row=3, column=3)
button_mode.grid(row=4,column=1)
button_switch.grid(row=4,column=2)
button_controller.grid(row=4,column=3)
button_switch2.grid(row=4,column=4)
button_sit.grid(row=3,column=4)
button_stand.grid(row=2,column=4)
button_up.grid(row=2, column=8)
button_down.grid(row=4, column=8)
button_right.grid(row=3, column=9)
button_left.grid(row=3, column=7)
button_headreset.grid(row=3,column=8)
button_b.grid(row=8, column=1)
button_p.grid(row=8, column=2)
button_jiggle.grid(row=8,column=3)
button_dance.grid(row=8,column=7)
button_belch.grid(row=8,column=8)
button_sneeze.grid(row=8,column=9)
scale.grid(row=3,column=5)

#turn round text
turnaroundlabel=Label(root,anchor=CENTER,text="Turn around")
turnaroundlabel.grid(row=4,column=5)

# elevation and azimuth label [positions]
latestcommandlabel=Label(root,anchor=CENTER,textvariable=latestcommand,width=25)
latestcommandlabel.grid(row=1,column=5)
latestcommand2label=Label(root,anchor=CENTER,textvariable=latestcommand2,width=25)
latestcommand2label.grid(row=2,column=5)

root.mainloop()  

if __name__ == '__main__':
    exit(0)     