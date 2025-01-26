import ollama
import requests

host="localhost"
port="11434"
url = f"http://{host}:{port}/api/chat"
model = "mistral"
headers = {"Content-Type": "application/json"}
data = {
        "model": 'mistral', #模型选择
        "options": {
            "temperature": 0.  #为0表示不让模型自由发挥，输出结果相对较固定，>0的话，输出的结果会比较放飞自我
         },
        "stream": False, #流式输出
        "messages": [{
            "role": "system",
            "content":"who are you"
        }] 
    }
response=requests.post(url,json=data,headers=headers,timeout=60)
res=response.json()
print(res)