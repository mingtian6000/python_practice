from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2',local_files_only=True, cache_folder='C:\\Users\\alice\\paraphrase-multilingual-MiniLM-L12-v2')

texts = [
    "猴子是一种灵长类动物，擅长攀爬树木，喜欢群居生活。它们主要以水果、树叶和小型昆虫为食，尤其是香蕉和桃子。",  # 样本1
    "西瓜是一种夏季常见的水果，外皮绿色带条纹，果肉多汁甜美。人们常在炎热天气食用西瓜解暑，西瓜的种子可以晒干后作为零食"         # 样本2
]
query = "猴子是什么"


embeddings = model.encode(texts)
query_embedding = model.encode(query)
#similarity check
cos_scores = util.cos_sim(query_embedding, embeddings)
print("相似度分数:", cos_scores)  