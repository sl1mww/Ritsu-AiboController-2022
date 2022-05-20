import json
import sys
import time
import urllib.request
import keyboard
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

def do_action():
    
    while True:
        if keyboard.is_pressed("w"):
            print("move forward")
            api_name="move_forward"
            data = '{"arguments":' '{"WalkSpeed":1,"WalkDistance":0.5}''}'

            post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
            req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
            
            with urllib.request.urlopen(req) as res:
                response = res.read()
            post_result = json.loads(response)
        if keyboard.is_pressed("s"):
            print("move backwards")
            api_name="move_forward"
            data = '{"arguments":' '{"WalkSpeed":1,"WalkDistance":-0.5}''}'

            post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
            req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
            
            with urllib.request.urlopen(req) as res:
                response = res.read()
            post_result = json.loads(response)
        if keyboard.is_pressed("a"):
            print("move to left")
            api_name="move_sideways"
            data = '{"arguments":' '{"WalkSpeed":2,"WalkDistance":0.5}''}'

            post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
            req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
            
            with urllib.request.urlopen(req) as res:
                response = res.read()
            post_result = json.loads(response)
        if keyboard.is_pressed("d"):
            print("move to right")
            api_name="move_sideways"
            data = '{"arguments":' '{"WalkSpeed":2,"WalkDistance":-0.5}''}'
            
            post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/'+ api_name + '/execute'
            req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
            
            with urllib.request.urlopen(req) as res:
                response = res.read()
            post_result = json.loads(response)
        
    

      
        # POST API
     

        '''
        executionId = post_result["executionId"]

        # Get Result of API execution
        get_result_url = BASE_PATH + '/executions/' + executionId
        TimeOut = 0
        while True:
            req = urllib.request.Request(get_result_url, headers=headers, method='GET')
            with urllib.request.urlopen(req) as res:
                response = res.read()
            get_result = json.loads(response)
            get_status = get_result["status"]

            print(get_status)

        '''
           
    
        
if __name__ == '__main__':
        do_action()
        exit(1)


root = Tk()

myLabel1 = Label(root, text="Hello World!")
myLabel2 = Label(root, text="My Name is Ian")

myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=0)

root.mainloop()