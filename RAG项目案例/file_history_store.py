"""
基于BaseChatMessageHistory类 创建FileChatMessageHistory类：历史信息存储、提取、清空
"""
# 0. 导包
import os
import json
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

# 1. 根据会话id，来获取FileChatMessageHistory对象
# session_id是文件名，FileChatMessageHistory对象就是那个文件
# session_id不同，对应的FileChatMessageHistory对象也不同，存储的历史信息也不同
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

# 2. 自己定义FileChatMessageHistory
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

    # 2.1 存储历史信息，模型回答后，自动调用
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

    # 2.2 提取历史信息，new_chain需要历史消息时自动调用
    @property  # @property装饰器将messages方法变成成员属性用，意味着调用时不需要加括号，直接写 self.messages
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  # 返回值就是：list[字典]，json.load()自带写读取文件功能，不需要f.read()
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    # 2.3 清除历史信息
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)