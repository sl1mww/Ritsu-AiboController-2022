import json
import sys
import time
import urllib.request
import keyboard
from curses import BUTTON2_CLICKED
from tkinter import *


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

def turn_around_clock():
    print("turn around clockwise")
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":-45}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def turn_around_anticlock():
    print("turn around anticlockwise")
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":45}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)


'''
def do_action():
    while True:
        if keyboard.is_pressed("w"):
            move_forward
        if keyboard.is_pressed("s"):
            move_backwards
        if keyboard.is_pressed("a"):
            move_left
        if keyboard.is_pressed("d"):
            move_right
        if keyboard.is_pressed("l"):
            turn_around_clock
        if keyboard.is_pressed("j"):
            turn_around_anticlock
            '''

data='{"arguments":{"ModeName":"DEVELOPMENT"}}'
def convert():
    if(button_mode['state']==DISABLED):
        button_mode["state"] = NORMAL
        button_switch["text"]="OFF"
        data='{"arguments":{"ModeName":"DEVELOPMENT"}}'

    elif (button_mode['state']==NORMAL):
        button_mode["state"]=DISABLED
        button_switch["text"]="ON"
        data='{"arguments":{"ModeName":"NORMAL"}}'

def set_mode(data):
    print("Setting mode...")

    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/set_mode' + '/execute '
    req = urllib.request.Request(post_url, data.encode(),headers=headers, method='POST')

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

root =Tk()
root.title("Basic W,A,S,D Movements")

#keyboards
root.bind('w', lambda event: move_forward())
root.bind('s', lambda event: move_backwards())
root.bind('a', lambda event: move_left())
root.bind('d', lambda event: move_right())
root.bind('e', lambda event: turn_around_clock())
root.bind('q', lambda event: turn_around_anticlock())

#??? what is this
def button_move():
    return

#virtual control buttons
button_w = Button(root, text="W", padx=30, pady=20, command=move_forward)
button_s = Button(root, text="S", padx=30, pady=20, command=move_backwards)
button_a = Button(root, text="A", padx=30, pady=20, command=move_left)
button_d = Button(root, text="D", padx=30, pady=20, command=move_right)
button_e = Button(root, text="↩️", padx=30, pady=20, command=turn_around_clock)
button_q = Button(root, text="↪️", padx=30, pady=20, command=turn_around_anticlock)
button_switch = Button(root, text="Mode", padx=10, pady=10)
#mode display
button_mode=Button(root,text="Developer Mode",state=DISABLED)
button_mode.config(height=1,width=10)
#switch button
button_switch = Button(root, text="On", padx=10, pady=10, command=lambda:[convert(),set_mode(data)])


#Position of buttons
button_w.grid(row=1, column=2)
button_s.grid(row=2, column=2)
button_a.grid(row=2, column=1)
button_d.grid(row=2, column=3)
button_q.grid(row=1, column=1)
button_e.grid(row=1, column=3)
button_mode.grid(row=3,column=1)
button_switch.grid(row=3,column=2)

root.mainloop()  

if __name__ == '__main__':
    exit(1)     