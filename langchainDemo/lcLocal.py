from langchain_ollama import OllamaLLM
from langchain_community.llms import Ollama

model = OllamaLLM(model="deepseek-r1:7b")
print(model)
model.invoke("Come up with 10 names for a song about parrots")

host="localhost" 
port="11434" 
llm=Ollama(base_url=f"http://{host}:{port}", model="deepseek-r1:7b",temperature=0)
res=llm.invoke("who are you")
print(res)
### above and below not work from my side...
#from langchain_ollama import ChatOllama
#chat_model = ChatOllama(model="llama3.1:8b")
#chat_model.invoke("Who was the first man on the moon?") 