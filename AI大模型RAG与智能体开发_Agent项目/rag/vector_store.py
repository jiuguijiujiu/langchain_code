# 0. 导包
import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from utils.config_handler import chroma_conf
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from model.factory import embed_model

# 1. 创建知识库VectorStoreService类
class VectorStoreService:
    # 1.1 初始化
    def __init__(self):
        # 1.1.1 创建chroma 向量库对象
        self.chroma = Chroma(
            collection_name=chroma_conf["collection_name"],             # 向量库名
            embedding_function=embed_model,                             # 嵌入模型
            persist_directory=chroma_conf["persist_directory"],         # 向量库存放位置
        )
        
        # 1.1.2 创建分割器对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )
    # 1.2 创建 获取检索器对象 方法
    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    # 1.3 创建 将文件保存到向量库（带去重功能） 方法
    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """
        # 1.3.1 检查md5值 是否已经存在于 md5文件中
        def check_md5_hex(md5_for_check: str):
            # 1.3.1.1 如果 保存md5值的文件 不存在
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False            # md5 不重复

            # 1.3.1.2 如果 保存md5值文件 存在，判断md5文件 是否存在重复md5值
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True     # md5 重复
                return False            # md5 不重复

        # 1.3.2 保存md5值 到md5文件中
        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        # 1.3.3 利用文件加载器 获取文件内容
        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        # 1.3.4 将data文件夹下的 允许文件的绝对路径 放到列表里
        allowed_files_path: tuple[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        # 1.3.5 循环 data目录下 每一个文件绝对路径
        for path in allowed_files_path:
            # 1.3.5.1 获取文件的MD5
            md5_hex = get_file_md5_hex(path)

            # 1.3.5.2 如果md5值 已经存在于 md5文件中，记录日志，结束本次循环，
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue


            try:
                # 1.3.5.3 加载器 加载文件
                documents: list[Document] = get_file_documents(path)
                # 1.3.5.4 如果加载的文件内容为空，记录日志，结束循环
                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                # 1.3.5.5 分割器对象 分割list[Document]
                split_document: list[Document] = self.splitter.split_documents(documents)

                # 1.3.5.6 为什么split_document会为空呢？
                # “加载出来的文档对象非空” 不等于 “里面包含有效的人类文字”，分割器会过滤文件内部的空白字符（\n...）或无法解析的乱码（图片...）
                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 1.3.5.7 将分割后的list[Document]存入向量库
                self.chroma.add_documents(split_document)

                # 1.3.5.8 保存md5值 到md5文件中
                save_md5_hex(md5_hex)
                # 1.3.5.9 记录日志
                logger.info(f"[加载知识库]{path} 内容加载成功")

            except Exception as e:
                # 1.3.5.10 如果在try中出现问题，记录日志，结束循环
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)      # exc_info：为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                continue

# 2. 测试
if __name__ == '__main__':
    # 2.1 创建 VectorStoreService类
    vs = VectorStoreService()
    # 2.2 保存知识到向量库
    vs.load_document()
    # 2.3 创建 检索器
    retriever = vs.get_retriever()
    # 2.4 使用invoke方法调用检索器
    res = retriever.invoke("迷路")
    # 2.5 查询结果返回list[Document]，所以循环查询检索出来的结果
    for r in res:
        print(r.page_content)
        print("-"*20)