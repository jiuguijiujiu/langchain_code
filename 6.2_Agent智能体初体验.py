# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent


# 1. 创建天气工具
@tool(description="查询天气")
def get_weather() -> str:
    return "晴天"

# 2. 创建agent对象
agent = create_agent(
    model=ChatTongyi(model="qwen3.7-max"),              # 模型
    tools=[get_weather],                                # 工具
    system_prompt="你是一个聊天助手，可以回答用户问题。",      # 系统提示词
)

# 3. 使用invoke方法调用agent对象
res = agent.invoke(
    {"messages":                                    # type: ignore
                [
                    {"role": "user", "content": "明天深圳的天气如何？"}
                ]
            }
)

# 4. 输出模型回复信息
for msg in res["messages"]:
    print(type(msg).__name__, msg.content)