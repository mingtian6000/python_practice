from sentence_transformers import SentenceTransformer
import chromadb
import ollama

client = chromadb.PersistentClient(path="ollama_rag_db")
collection = client.create_collection(name="knowledge")
documents = [
    "猴子是灵长类动物，擅长攀爬树木。",
    "西瓜是夏季水果，果肉多汁甜美。",
    "太阳系的中心是太阳。"
]

def get_ollama_embedding(text, model="mistral"):
    response = ollama.embeddings(model=model, prompt=text)
    return response["embedding"]


def retrieve(query, top_k=2):
    query_embed = get_ollama_embedding(query)
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=top_k
    )
    return results["documents"][0]

def generate_answer(query):
    context = "\n".join(retrieve(query))
    prompt = f"""基于以下上下文回答问题：
    {context}
    问题: {query}
    答案:"""
    response = ollama.generate(
        model="llama3",  # 替换为你的生成模型（如 mistral）
        prompt=prompt
    )
    return response["response"]

for i, doc in enumerate(documents):
    embedding = get_ollama_embedding(doc)  
    collection.add(
        documents=[doc],
        embeddings=[embedding],
        ids=[f"doc_{i}"]
    )
query = "猴子有什么特点？"
print(generate_answer(query))