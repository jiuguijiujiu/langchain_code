"""
知识库
"""
# 0. 导包
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

# 1. 创建md5工具函数（知识去重工具）
# 1.1 将接收的字符串 转为 md5值字符串
def get_str_to_md5(input_str: str, encoding='utf-8'):
    # 1.1.1 将字符串先转为bytes（字节串）
    str_bytes = input_str.encode(encoding=encoding)

    # 1.1.2 创建md5对象
    md5_obj = hashlib.md5()
    # 1.1.3 加载字节串（传入即将要转换的字节数组）
    md5_obj.update(str_bytes)
    # 1.1.4 转换字节串，得到md5的十六进制字符串
    md5 = md5_obj.hexdigest()

    # 1.1.5 返回md5值字符串
    return md5

# 1.2 检查md5值字符串是否在 md5文件中重复
def check_md5(md5: str):
    """
    :return: False(不重复)  True(重复）
    """
    # 1.2.1 先判断存储md5值的文件是否存在
    if not os.path.exists(path=config.md5_path):
        # 1.2.1.1 进入这，表示文件不存在，则创建文件
        open(file=config.md5_path, mode='w', encoding='utf-8').close()
        # 1.2.1.2 文件都没有，肯定不重复，返回False
        return False
    else:
        # 1.2.2 进入这，表示文件存在，则判断是否重复
        for line in open(file=config.md5_path, mode='r', encoding='utf-8').readlines():
            line = line.strip()     # 去除字符串首尾的空白字符（空格、制表符、换行符等）
            if line == md5:
                # 1.2.2.1 进入这，说明md5值字符串 在md5文件中已经存在，返回Ture
                return True
        # 1.2.3 循环结束后，没找到重复的md5值字符串，返回False
        return False

# 1.3 保存md5值字符串到 md5文件中
def save_md5(md5: str):
    with open(file=config.md5_path, mode='a', encoding="utf-8") as f:
        f.write(md5 + '\n')

# 2. 创建KnowledgeBaseService类
class KnowledgeBaseService:
    # 2.1 初始化
    def __init__(self):
        # 2.1.1 如果存储Chrom数据库的文件夹不存在则创建，如果存在则跳过
        os.makedirs(name=config.persist_directory, exist_ok=True)

        # 2.1.2 创建Chroma向量数据库对象
        self.chroma = Chroma(
            collection_name=config.collection_name,                                 # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),      # 嵌入模型
            persist_directory=config.persist_directory,                             # 存储数据库的文件夹
        )

        # 2.1.3 创建字符串文本分割器对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,           # 分割后的文本段的最大长度
            chunk_overlap=config.chunk_overlap,     # 允许连续文本段之间的字符重叠数量
            separators=config.separators,           # 段落划分的依据符号
            length_function=len,                    # 长度统计的依据函数
        )

    # 2.2 去重 + 存储知识的动作
    def store_knowledge(self, text: str, file_name):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        # 2.2.1 将字符串 转换为 md5值字符串
        md5 = get_str_to_md5(text)

        # 2.2.2 检查md5值字符串是否在 md5文件中重复
        if check_md5(md5):
            # 2.2.2.1 进入这里，说明md5值字符串重复，不需要进行存储，返回[跳过]
            return "[跳过]内容已经存在知识库中"

        # 到这里，说明md5值字符串不在md5文件中，进行存储操作
        # 2.2.3 字符段长度超过设定值，则分割字符串
        if len(text) > config.max_split_char_number:
            text_chunks: list[str] = self.spliter.split_text(text=text)
        else:
            text_chunks = [text]

        # 2.2.4 准备元数据
        metadata = {
            "source": file_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),                # 2025-01-01 10:00:00
            "operator": "小曹",
        }

        # 2.2.5 存入知识到向量库
        self.chroma.add_texts(
            texts=text_chunks,                              # 需要存储的知识：list[str]
            metadatas=[metadata for _ in text_chunks]       # 为每个字符串段落准备元数据
        )

        # 2.2.6 存储md5值字符串到md5文件中
        save_md5(md5)

        # 2.2.7 存储成功，返回[成功]
        return "[成功]内容已经成功载入向量库"

# 3. 测试
if __name__ == '__main__':
    # 3.1 创建知识库服务对象
    service = KnowledgeBaseService()
    # 3.2 用store_knowledge方法调用知识库服务对象，返回 [跳过] 或 [成功]
    r = service.store_knowledge(text="周杰轮222", file_name="testfile")
    print(r)