# 0. 导包
# from langchain_community.llms.tongyi import Tongyi
from langchain_ollama import OllamaLLM

# 1. 创建模型对象
# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是大语言模型
# model = Tongyi(model = 'qwen-max')
model = OllamaLLM(model = 'qwen3:4b')

# 2. 通过invoke方法去调用模型
res = model.invoke(input = '你是谁？')

# 3. 输出模型回复结果
print(res)