# 0. 导包
import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 1. 获取文件内容的 md5字符串（十六进制字符串）
def get_file_md5_hex(filepath: str):
    # 1.1 如果文件不存在，则记录日志，直接结束
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return
    # 1.2 如果输入不是文件类型，则记录日志，直接结束
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return
    # 1.3 创建md5对象
    md5_obj = hashlib.md5()
    # 1.4 读取文件最多4KB，避免文件过大爆内存
    chunk_size = 4096
    # 1.5 将文本内容转为md5值字符串
    try:
        with open(filepath, "rb") as f:             # 必须二进制读取，因为要先将字符串转为字节串，才能转为md5值字符串
            # 1.5.1 循环加载 字节串 到 md5对象中
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            """
            # 等同于上面写法
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)               # 加载 字节串 到 md5对象中
                chunk = f.read(chunk_size)
            """
            # 1.5.2 使用hexdigest调用md5对象，进行 字节串 转为 md5值字符串
            md5_hex = md5_obj.hexdigest()
            # 1.5.3 返回md5值字符串
            return md5_hex
    except Exception as e:
        # 如果转换中出错，记录日志，返回None
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None

# 2. 返回文件夹内的文件列表，allowed_types：允许的文件后缀
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    # 1. 创建文件空列表
    files = []
    # 2. 如果传入的不是文件夹类型，则记录日志，直接返回allowed_types
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types
    # 3. 循环输出文件夹里的文件
    for f in os.listdir(path):                          # os.listdir(path)：将文件夹里的每个文件绝对路径放到一个列表里
        # 3.1 判断文件是否是允许的文件后缀
        if f.endswith(allowed_types):                   # f.endswith(allowed_types)：接收tuple[str]类型
            files.append(os.path.join(path, f))
    # 4. 返回元组类型
    return tuple(files)

# 3. 创建pdf加载器对象，并用load方法调用加载器，得到list[Document]
def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()

# 3. 创建txt加载器对象，并用load方法调用加载器，得到list[Document]
def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()
