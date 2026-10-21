# 0. 导包
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf
from abc import ABC, abstractmethod
from typing import Optional

# 1. 定义一个基础工厂类
# ABC 和 @abstractmethod 的意思是：定规矩
# 这个类规定：只要你是我的“子工厂”，你就必须得有一个叫 generator 的方法，用来生产模型，不写就会报错
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

# 2. 造两个具体的具体工厂类
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        # 2.1 创建模型对象并返回
        return ChatTongyi(model=rag_conf["chat_model_name"])

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

# 3. 创建类，调用generator方法，得到模型对象
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()