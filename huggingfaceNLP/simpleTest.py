#vector DB demo
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                documents.append(file.read())
        elif filename.endswith(".pdf"):
            # 使用 PyPDF2 或 pdfplumber 提取文本
            pass
    return documents

def search(query, top_k=1):

    query_embedding = model.encode([query])

    _, indices = index.search(np.array(query_embedding).astype('float32'), top_k)

    results = []
    for idx in indices[0]:
        results.append(documents[idx])
    return results


documents = load_documents("C:\\Users\\alice\\vscodeProject\\python_basic\\huggingfaceNLP")

model = SentenceTransformer('all-MiniLM-L6-v2',local_files_only=True, cache_folder='C:\\Users\\alice\\all-MiniLM-L6-v2')

document_embeddings = model.encode(documents)
# 创建 FAISS 索引
dimension = 384  # all-MiniLM-L6-v2 的向量维度
index = faiss.IndexFlatL2(dimension)

index.add(np.array(document_embeddings).astype('float32')) #保存到内存里
faiss.write_index(index, "document_index.faiss") #持久化盘在当前文件夹

query = "猴子是什么？"
results = search(query, 1)
for result in results:
    print(result)