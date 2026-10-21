# 0. 导包
from openai import OpenAI

# 1. 创建openai对象
client = OpenAI(
    # 如果没有配置环境变量，请使用用阿里云百炼API Key：api_key="sk-xxx"
    # api_key="sk-xxx",
    base_url="https://ws-7xn36acu51vwzxvg.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2. 设置提示词
messages = [{"role": "user", "content": "你是谁？"}]

# 3. 调用模型
completion = client.chat.completions.create(            # type: ignore
    model="deepseek-v4.1-flash",            # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)

# 4. 输出回复结果
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)