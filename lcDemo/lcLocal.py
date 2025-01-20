from langchain_ollama import OllamaLLM

model = OllamaLLM(model="mistral")
model.invoke("The first man on the moon was ...")

### above and below not work from my side...
#from langchain_ollama import ChatOllama
#chat_model = ChatOllama(model="llama3.1:8b")
#chat_model.invoke("Who was the first man on the moon?")