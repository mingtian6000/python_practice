import ollama

host="localhost"
port="11434"
client= ollama.Client(host=f"http://{host}:{port}")
res=client.chat(model="mistral",
                messages=[{"role": "user","content": "who are you"}],
                options={"temperature":0})
 
print(res)