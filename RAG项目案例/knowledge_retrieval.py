"""
知识检索
"""
# 0. 导包
from langchain_chroma import Chroma
import config_data as config

# 1. 创建KnowledgeRetrieval类
class KnowledgeRetrieval:
    # 1.1 初始化
    def __init__(self, embedding):
        """
        :param embedding: 嵌入模型的传入
        """
        # 1.1.1 创建嵌入模型对象
        self.embedding = embedding

        # 1.1.2 创建Chroma向量库对象
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    # 1.2 返回 创建的检索器对象
    def get_retriever(self):
        """返回向量检索器，方便加入chain"""
        return self.chroma.as_retriever(search_kwargs={"k": config.top_k})

# 2. 测试
if __name__ == '__main__':
    # 2.1 导包
    from langchain_community.embeddings import DashScopeEmbeddings
    # 2.2 创建知识检索对象，并调用get_retriever方法，得到 检索器对象
    retriever = KnowledgeRetrieval(embedding=DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()
    # 2.2 使用invoke方法调用检索器，返回list[Document]
    res = retriever.invoke(input="我的体重180斤，尺码推荐")
    print(res)

