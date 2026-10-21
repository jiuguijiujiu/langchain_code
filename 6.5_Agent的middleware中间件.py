# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model
from langchain.agents.middleware import wrap_model_call, wrap_tool_call
from langgraph.runtime import Runtime

# 1. 创建查询天气工具
@tool(description="查询天气，传入城市名称字符串，返回字符串天气信息")
def get_weather(city: str) -> str:
    return f"{city}天气：晴天"

# 2. 创建中间件（钩子函数）
"""
1. agent执行前
2. agent执行后
3. model执行前
4. model执行后
5. 工具执行中
6. 模型执行中
"""

# 2.1 创建节点式钩子函数
@before_agent
def log_before_agent(agentstate: AgentState, runtime: Runtime) -> None:
    # AgentState 是一个类型字典（TypedDict），你可以把它理解为 Agent 在当前时刻的内部状态快照。它包含了 Agent 运行过程中需要携带的所有数据，其中最关键的是 messages 字段
    # Runtime 是一个运行时对象，它提供了本次 Agent 执行过程中的全局信息和工具。可以把它看成是 Agent 运行时的“后台工具箱”，包含了与业务逻辑无关的运行环境细节
    # agentstate['messages']里面装了聊天信息
    """
    [
        HumanMessage(content='深圳今天的天气如何呀，如何穿衣', ...)
    ]
    """
    print(agentstate)
    print(runtime)
    print(f"[before agent]agent启动，并附带{len(agentstate['messages'])}消息")

@after_agent
def log_after_agent(agentstate: AgentState, runtime: Runtime) -> None:
    # agentstate['messages']里面装了聊天信息
    """
    [
        HumanMessage(content='深圳今天的天气如何呀，如何穿衣'),
        AIMessage(content=''),
        toolMessage(content='深圳天气：晴天'),
        AIMessage(content='深圳今天是晴天')
    ]
    """
    print(f"[after agent]agent结束，并附带{len(agentstate['messages'])}消息")

@before_model
def log_before_model(agentstate: AgentState, runtime: Runtime) -> None:
    print(f"[before_model]模型即将调用，并附带{len(agentstate['messages'])}消息")

@after_model
def log_after_model(agentstate: AgentState, runtime: Runtime) -> None:
    print(f"[after_model]模型调用结束，并附带{len(agentstate['messages'])}消息")

# 2.2 创建包装式钩子函数
@wrap_model_call
def model_call_hook(request, handler):
    # 接收request, handler两对象
    # request：请求包，封装了这次调用模型要用的完整参数
    """
    request.model          # 用哪个模型
    request.messages       # 消息列表
    request.system_prompt  # 系统提示
    request.tools          # 可用工具
    request.tool_choice    # 工具选择策略
    ...
    """
    # handler：执行请求包的处理器
    print("模型调用啦")
    return handler(request)

@wrap_tool_call
def monitor_tool(request, handler):
    # 接收request, handler两对象
    # request：请求包，封装了这次调用工具要用的完整参数
    """
    request.tool_call           # 工具调用的完整信息
    request.tool_call["name"]   # 工具名，比如 "get_weather"
    request.tool_call["args"]   # 参数，比如 {"city": "北京"}
    request.tool_call["id"]     # 调用 ID
    """
    # handler：执行请求包的处理器
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行传入参数：{request.tool_call['args']}")
    return handler(request)

# 3. 创建agent对象
agent = create_agent(
    model=ChatTongyi(model="qwen3.7-max"),
    tools=[get_weather],
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, model_call_hook, monitor_tool]
)

# 4. 用invoke方法调用agent
res = agent.invoke(input={"messages": [{"role": "user", "content": "深圳今天的天气如何呀，如何穿衣"}]})
print("*" * 50 + "\n", res)
print(type(res))
# res = {"messages": [BaseMessage, BaseMessage, BaseMessage, ...]}