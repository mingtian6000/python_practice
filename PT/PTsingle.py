from datetime import datetime
import string
import random, re, time, requests

def call_api(url, data):
    response = requests.post(url, data=data, timeout=10)
    print("current time: ", datetime.now()), "posted 1 request"
    return response.status_code

def send_requests(url, data, tps, duration):
    interval=1/tps  # time intervals between requests
    end_time = time.time() + duration
    while time.time() < end_time:  # like in java. constant volumn, but this is way is not like in real-world
        call_api(url, data)
        time.sleep(interval)
    
    
def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))   

def change_data(payload):
    e2eid = random_string(23)
    payload = str.replace("#E2EID#", e2eid, payload)
    print("sending payload", payload)
    return payload
    # it depends on your real payload, may have multiple fields, or nested fields, etc.

def main():
    api_url = "http://localhost:8080/api/v1/endpoint" # your test url
    data="""
    {
        "header": {
            "e2eid": "#E2EID#",
            "timestamp": "2020-12-12 12:12:12"
        },
        "body": {
            "name": "test",
            "age": 20
        },
        "error_code": 0
    }
    """
    payload = change_data(data)
    print("staring ph1: 2TPS for 1mins")
    send_requests(api_url, payload, 2, 60) # 2TPS for 1min
    print("staring ph2: 5TPS for 2mins")
    send_requests(api_url, payload, 5, 120) # 5TPS for 2min
    print("staring ph3: 10TPS for 3mins")
    send_requests(api_url, payload, 10, 180) # 10TPS for 3min