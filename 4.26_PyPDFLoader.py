# 0. 导包
from langchain_community.document_loaders import PyPDFLoader

# 1. 创建PyPDF加载器对象
loader = PyPDFLoader(
    file_path="./数据/pdf2.pdf",      # 文件路径，必填
    mode="single",                   # 读取模式，默认是page模式，每个页面形成一个Document文档对象，single模式，不管有多少页，只返回1个Document对象的列表
    password="itheima"               # 文件密码
)

# 2. 使用lazy_load方法调用PyPDF加载器
i = 0
for doc in loader.lazy_load():
    i += 1
    print(doc)
    print("=" * 20, i)