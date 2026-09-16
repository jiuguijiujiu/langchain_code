# 导包
# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_ollama import ChatOllama

# 创建模型对象
# chat = ChatTongyi(model = 'qwen3-max')
chat = ChatOllama(model = 'qwen3:4b')

# 准备消息list
message = [
    # (角色，内容)  角色：system/human/ai
    ("system", "你是一个边塞诗人。"),
    ("human", "写一首唐诗。"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照你上一个回复的格式，在写一首唐诗。")
]

# 流式输出
for chunk in chat.stream(input = message):
    print(chunk.content, end = '', flush = True)