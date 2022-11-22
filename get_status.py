#get api status
import json
import sys
import time
import urllib.request

headers = {
'Authorization': 'Bearer ', # insert access token after "Bearer " 
} 
BASE_PATH = 'https://public.api.aibo.com/v1' 
DEVICE_ID = "" #input device ID for particular aibo
TIME_OUT_LIMIT = 5 #time limit for changing from developer-normal (vice-versa)

def do_action(executionID):
    post_url = BASE_PATH + '/v1/' + '/executions/' + executionID

    # Get Result of API execution
    get_result_url = BASE_PATH + '/executions/' + executionID

    #TimeOut = 0
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
'''
 TimeOut += 1
        if TimeOut > TIME_OUT_LIMIT:
            print("Time out")
            break

        time.sleep(1)
'''
       

if __name__ == '__main__':
    length = len(sys.argv)
    if length == 2:
        do_action(sys.argv[1])
    else :
        print("execute_action_api.py <action api name> <parameters>")
        exit(1)