import os
from langchain_community.chat_models.tongyi import ChatTongyi

chat = ChatTongyi(model="qwen3-max")
try:
    res = chat.invoke("你好")
    print(res.content)
except Exception as e:
    print(f"连接失败: {e}")