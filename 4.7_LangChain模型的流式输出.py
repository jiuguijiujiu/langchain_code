# 1. 导包
# from langchain_community.llms.tongyi import Tongyi
from langchain_ollama import OllamaLLM

# 2. 调用模型
# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
# model = Tongyi(model = 'qwen-max')
model = OllamaLLM(model = 'qwen3.5:9b')

# 3. 询问问题
# 调用invoke向模型提问
# res = model.invoke(input = '你是谁？')
res = model.stream(input = '你是谁？')

for chunk in res:
    print(chunk, end = "", flush = True)