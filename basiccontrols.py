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

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":-180}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

def turn_around_anticlock():
    print("turn around anticlockwise")
    api_name="turn_around"

    data = '{"arguments":{"TurnSpeed":2,"TurnAngle":180}}'
    
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)

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

root = Tk()
root.title("Basic W,A,S,D Movements")

def button_move():
    return

button_w = Button(root, text="W", padx=30, pady=20, command=move_forward)
button_s = Button(root, text="S", padx=30, pady=20, command=move_backwards)
button_a = Button(root, text="A", padx=30, pady=20, command=move_left)
button_d = Button(root, text="D", padx=30, pady=20, command=move_right)
button_j = Button(root, text="L", padx=30, pady=20, command=turn_around_clock)
button_l = Button(root, text="J", padx=30, pady=20, command=turn_around_anticlock)

button_w.grid(row=1, column=2)
button_s.grid(row=2, column=2)
button_a.grid(row=2, column=1)
button_d.grid(row=2, column=3)
button_l.grid(row=2, column=4)
button_j.grid(row=2, column=5)

root.mainloop()
        
if __name__ == '__main__':
        do_action()
        exit(1)     