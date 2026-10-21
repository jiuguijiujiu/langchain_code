# 0. 导包
import os, json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage

# message_to_dict：单个消息对象（BaseMessage对象） -> 字典
# messages_from_dict：[字典、字典...]  -> [消息对象、消息对象...]
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类

# 1. 自己定义FileChatMessageHistory
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id            # 会话id
        self.storage_path = storage_path        # 存储历史信息文件的 父路径
        self.file_path = os.path.join(self.storage_path, self.session_id)       # 存储历史信息文件的 路径

        # 确保文件 父路径 是否存在，不存在则创建
        # os.path.dirname(self.file_path)提取出文件路径中的目录部分（即去掉文件名，只留文件夹路径）
        # exist_ok，设置为 False（默认），当目录已经存在时，程序会抛出 FileExistsError 报错崩溃
        # exist_ok，设置为 True，意思是“如果目录已经存在，就当无事发生，不要报错，继续往下执行”
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # 1. 存储历史信息，模型回答后，自动调用
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list、tuple
        all_messages = list(self.messages)          # 已有的历史信息
        all_messages.extend(messages)               # 新传入的历史信息和已有的历史信息融合成一个list

        # 将历史信息写入到本地文件中
        # 历史信息 -> 二进制
        # 先将BaseMessage消息转为字典，在借助json模块以json字符串写入文件
        # message_to_dict：单个消息对象（BaseMessage对象） -> 字典
        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)

        new_messages = [message_to_dict(message) for message in all_messages]
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(obj = new_messages, fp = f)      # json.dump()自带写入文件功能，不需要f.write()

    # 2. 提取历史信息，conversation_chain需要历史消息时自动调用
    @property  # @property装饰器将messages方法变成成员属性用，意味着调用时不需要加括号，直接写 self.messages
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  # 返回值就是：list[字典]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    # 3. 清除历史信息
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

# 2. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 3. 创建提示词模板对象
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

# 5. 创建链A（无记忆功能）
base_chain = prompt | print_prompt | model | str_parser

# 6. 根据会话id，来获取FileChatMessageHistory对象
# session_id是文件名，FileChatMessageHistory对象就是那个文件
# session_id不同，对应的FileChatMessageHistory对象也不同，存储的历史信息也不同
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./数据")

# 7. 基于链A基础上，创建一个带有记忆功能的新链B
conversation_chain = RunnableWithMessageHistory(
    runnable = base_chain,                              # 没有记忆功能的链A
    get_session_history=get_history,                    # 存储历史信息的对象 ——> FileChatMessageHistory对象
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