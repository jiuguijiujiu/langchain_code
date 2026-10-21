# 0. 导包
from openai import OpenAI

# 1. 创建openai对象
client = OpenAI(
    base_url="https://ws-7xn36acu51vwzxvg.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2. 调用模型
client.chat.completions.creat(
    model="deepseek-v4.1-flash",
    messages=[
        {}
    ]
)