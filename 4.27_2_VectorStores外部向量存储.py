# 0. 导包
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
# 确保 langchain-chroma chromadb 这两个库安装了的，没有的话请pip install langchain-chroma chromadb
from langchain_chroma import Chroma     # Chroma 向量数据库（轻量级）

# 1. 加载文件
# 1.1 创建CSV加载器对象
loader = CSVLoader(
    file_path="./数据/info.csv",
    csv_args={
        'delimiter': ','            # 分隔符
    },
    encoding="utf-8",
    source_column="source",         # 指定本条数据的来源，设置元数据（metadata）
)
# 1.2 使用load调用数据加载器
documents = loader.load()

# 2. 存储向量数据
# 2.1 创建Chroma对象
vector_store = Chroma(
    collection_name="test",                         # 给Chroma对象起个名字，类似数据库的表名称
    embedding_function=DashScopeEmbeddings(),       # 嵌入模型
    persist_directory="./chroma_db"                 # 指定存放Chroma对象的文件夹
)

# 2.2 向量存储的 新增、删除、检索
# 新增
vector_store.add_documents(
    documents=documents,                                    # 被添加的文档，类型：list[Document]
    ids=["id"+str(i) for i in range(1, len(documents)+1)]   # 给添加的文档提供id，类型：list[str]：[id1, id2, id3, id4, ...]
)

# 删除，传入[id, id...]
vector_store.delete(
    ids=["id1", "id3"]
)

# 检索，返回类型list[Document]
result = vector_store.similarity_search(
    query="传智教育",
    k=2                         # 检索的结果要几个
)
print(result)