# 导包
# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 创建模型对象
# chat = ChatTongyi(model = 'qwen3-max')
chat = ChatOllama(model = 'qwen3:4b')

# 准备消息list
message = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，在写一首唐诗。")
]

# 流式输出
for chunk in chat.stream(input = message):
    print(chunk.content, end = '', flush = True)