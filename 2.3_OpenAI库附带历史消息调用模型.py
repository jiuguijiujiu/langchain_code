# 0. 导包
from openai import OpenAI

# 1. 创建openai对象
client = OpenAI(
    base_url="https://ws-7xn36acu51vwzxvg.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2. 调用模型
response = client.chat.completions.create(                  # type: ignore
    model = 'deepseek-v4.1-flash',
    messages = [
        {"role": "system", "content": "你是AI助理，回答很简洁"},
        {"role": "user", "content": "小明有2条宠物狗"},
        {"role": "assistant", "content": "好的"},
        {"role": "user", "content": "小红有3只宠物猫"},
        {"role": "assistant", "content": "好的"},
        {"role": "user", "content": "总共有几个宠物？"}
    ],
    stream = True       # 开启了流式输出的功能
)

# 3. 输出模型回复结果
# print(response.choices[0].message.content)

for chunk in response:
    # 1. 防御：跳过没有 choices 的收尾包
    if not chunk.choices:
        continue

    # 2. 防御：content 可能为 None
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end = '', flush = True)                # flush=True立刻刷新缓冲区