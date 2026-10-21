"""
与机器人聊天的底层实现代码
"""
# 0. 导包
import config_data as config
from langchain_core.documents import Document
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from knowledge_retrieval import KnowledgeRetrieval
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history

# 1. 自定义函数：输出提示词内容
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

# 2. 创建RagService类
class RagService:
    # 2.1 初始化
    def __init__(self):
        # 2.1.1 创建聊天模型对象
        self.chat_model = ChatTongyi(model=config.chat_model_name)

        # 2.1.2 创建聊天提示词模板对象
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}")
            ]
        )

        # 2.1.3 创建知识检索器对象
        self.retriever = KnowledgeRetrieval(embedding=DashScopeEmbeddings(model=config.embedding_model_name)).get_retriever()

        # 2.1.4 自动执行__get_chain私有方法，只给出最终的执行链
        self.chain = self.__get_chain()

    # 2.2 创建__get_chain私有化方法
    def __get_chain(self):
        """返回最终执行链"""
        # 2.2.1 格式化 为知识检索器：dict——>str，因为知识检索器只接收str类型
        def format_for_retriever(input_dict: dict) -> str:
            return input_dict["input"]

         # 2.2.2 提取知识检索结果中有用的信息，并转为字符串
        def format_document(docs: list[Document])->str:
            if not docs:
                return "无相关参考资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        # 2.2.3 格式化 为提示词模板
        # 将{'input': {‘input’：str, 'history': list[BaseMessage]}, 'context':str} 转为 {'input': str, 'context': str, 'history': list[BaseMessage]}
        def format_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        # 2.2.4 创建链A（无记忆）
        chain = ({"input": RunnablePassthrough(),"context": RunnableLambda(format_for_retriever) | self.retriever | format_document}
                 | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        # 2.2.5 基于链A基础上，创建一个带有记忆功能的新链B
        new_chain = RunnableWithMessageHistory(
            runnable=chain,                             # 没有记忆功能的链
            get_session_history=get_history,            # 存储历史信息的对象 ——> FileChatMessageHistory对象
            input_messages_key="input",                 # 用户输入在模板中的信息占位符
            history_messages_key="history",             # 用户输入在模板中的历史信息占位符
        )

        # 2.2.6 返回执行链
        return new_chain

# 3. 测试
if __name__ == '__main__':
    # 1. 配置LangChain里的参数，且为固定格式：为当前程序配置所属的session_id参数
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

    # 2. 用invoke方法调用执行链
    # 如果是带有记忆的链，传入input参数的一定是字典，不能是字符串
    # 因为当invoke时，RunnableWithMessageHistory对象会自动将{"input": str}变成{'input': str, 'history': list[BaseMessage]}
    # 如果只传入字符串，则加入不了history，程序会报错
    res = RagService().chain.invoke(input={"input": "针织毛衣如何保养？"}, config=session_config)
    print(res)