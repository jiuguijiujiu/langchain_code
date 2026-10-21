# 0. 导包
from openai import OpenAI

# 1. 创建openai对象
client = OpenAI(
    base_url="https://ws-7xn36acu51vwzxvg.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2. 调用模型
response = client.chat.completions.create(
    model = 'deepseek-v4.1-flash',
    messages = [                                                # type: ignore
        {"role": "system", "content": "你是一个Python编程专家，并且不说废话简单回答"},
        {"role": "assistant", "content": "好的，我是编程专家，并且话不多，你要问什么？"},
        {"role": "user", "content": "输出1-10的数字，使用python代码"}
    ]
)

# 3. 输出模型回复结果
# print(response)
print(response.choices[0].message.content)