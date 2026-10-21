# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 1. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 2. 创建提示词模板对象
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题。对话历史：{chat_history}，用户提问：{input}，请回答"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

# 3. 创建输出解析器对象
str_parser = StrOutputParser()

# 4. 自定义函数，输出提示词模板
def print_prompt(full_prompt):
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt

# 5. 创建链A（没有记忆功能）
base_chain = prompt | print_prompt | model | str_parser

# 6. 根据会话id，来获取InMemoryChatMessageHistory对象
store = {}      # key就是session_id，value就是InMemoryChatMessageHistory对象
# session_id不同，对应的InMemoryChatMessageHistory对象也不同，存储的历史信息也不同
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 7. 基于链A基础上，创建一个带有记忆功能的新链B
conversation_chain = RunnableWithMessageHistory(
    runnable = base_chain,                              # 没有记忆功能的链A
    get_session_history=get_history,                    # 存储历史信息的工具 ——> InMemoryChatMessageHistory对象
    input_messages_key="input",                         # 用户输入在模板中的信息占位符
    history_messages_key="chat_history"                 # 用户输入在模板中的历史信息占位符
)

# 8. 测试
if __name__ == '__main__':
    # 1. 配置LangChain里的参数，且为固定格式：为当前程序配置所属的session_id参数
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    # 2. 用invoke方法调用链
    res = conversation_chain.invoke(input = {"input": "小明有2个猫"}, config = session_config)
    print("第1次执行：", res)
    res = conversation_chain.invoke(input = {"input": "小刚有1只狗"}, config = session_config)
    print("第2次执行：", res)
    res = conversation_chain.invoke(input = {"input": "总共有几个宠物"}, config = session_config)
    print("第3次执行：", res)