# 0. 导包
# from langchain_community.embeddings import DashScopeEmbeddings
from langchain_ollama import OllamaEmbeddings

# 1. 创建模型对象
# model = DashScopeEmbeddings()     #  不传参，model默认用的是 text-embeddings-v1
model = OllamaEmbeddings(model = 'qwen3-embedding:4b')

# 2. 不用invoke stream调用模型，用embed_query、embed_documents调用模型
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你", "我稀饭你", "晚上吃啥"]))