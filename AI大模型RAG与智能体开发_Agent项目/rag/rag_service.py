"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
# 0. 导包
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model.factory import chat_model
from utils.prompt_loader import load_rag_prompts
from rag.vector_store import VectorStoreService

# 1. 自定义函数：输出提示词
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

# 2. 创建 RagSummarizeService类：聊天功能
class RagSummarizeService:
    # 2.1 初始化
    def __init__(self):
        self.vector_store = VectorStoreService()                                    # 创建知识库对象
        self.retriever = self.vector_store.get_retriever()                          # 创建检索器对象
        self.prompt_text = load_rag_prompts()                                       # 加载rag提示词
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)       # 创建提示词模板
        self.model = chat_model                                                     # 创建模型对象
        self.chain = self._init_chain()                                             # 创建chain属性：私有方法_init_chain的接口

    # 2.2 创建私有方法_init_chain：创建链
    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    # 2.3 创建 检索器对象检索 方法
    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    # 2.4 用户 给出问题，链 返回回复
    def rag_summarize(self, query: str) -> str:
        # 2.4.1 获取检索器检索的结果
        context_docs = self.retriever_docs(query)

        # 2.4.2 处理检索器检索的结果：list[Document] -> str
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        # 2.4.3 用invoke方法调用chain，并返回结果
        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )

# 3. 测试
if __name__ == '__main__':
    # 3.1 创建RagSummarizeService类
    rag = RagSummarizeService()
    # 3.2 聊天
    print(rag.rag_summarize("小户型适合哪些扫地机器人"))
