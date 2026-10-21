# 0. 导包
# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_ollama import ChatOllama

# 1. 创建模型对象
# chat = ChatTongyi(model = 'qwen3.7-max')
chat = ChatOllama(model = 'qwen3:4b')

# 2. 设置提示词
message = [
    # (角色，内容)  角色：system/human/ai
    ("system", "你是一个边塞诗人。"),
    ("human", "写一首唐诗。"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照你上一个回复的格式，再写一首唐诗。")
]

# 3. 通过stream方法调用模型
for chunk in chat.stream(input = message):        # 返回的是Message类
    # 4. 输出模型回复结果
    print(chunk.content, end = '', flush = True)