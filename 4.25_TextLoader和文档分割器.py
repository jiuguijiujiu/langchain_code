# 0. 导包
from langchain_community.document_loaders import TextLoader
# pip install langchain_text_splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 创建Text加载器对象
loader = TextLoader(
    file_path = "./数据/Python基础语法.txt",
    encoding="utf-8")

# 2. 使用load方法调用Text加载器
docs = loader.load()  # [Document]

# 3. 创建文本分割器对象
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,                 # 允许段落的最大字符数
    chunk_overlap=50,               # 允许两个相邻段落之间重叠字符数
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],       # 段落分割的依据符号
    length_function=len,            # 统计字符数的依据函数
)

# 4. 用split_documents方法调用文本分割器
split_docs = splitter.split_documents(docs)
print(len(split_docs))
for doc in split_docs:
    print("=" * 20)
    print(doc)
    print("=" * 20)