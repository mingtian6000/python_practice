import requests
import time
from concurrent.futures import ThreadPoolExecutor

def send_requests(url, data, tps, duration):
    interval=1/tps  # time intervals between requests
    end_time = time.time() + duration
    while time.time() < end_time:  # like in java. constant volumn, but this is way is not like in real-world
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("posted 1 request")
        time.sleep(interval)


def main():
    URL_A="http://localhost:8080/api/v1/endpoint1"
    URL_B="http://localhost:8080/api/v1/endpoint2"
    URL_C="http://localhost:8080/api/v1/endpoint3"
    
    DATA_A = {"key_A":"value_A"}
    DATA_B = {"key_B":"value_B"}
    DATA_C = {"key_C":"value_C"}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        futures.append(executor.submit(send_requests, URL_A, DATA_A, 5, 3*60))
        futures.append(executor.submit(send_requests, URL_B, DATA_B, 3, 3*60))
        futures.append(executor.submit(send_requests, URL_C, DATA_C, 9, 3*60))
        for future in futures:
            print(future.result())
            
if __name__ == "__main__":
    main()
