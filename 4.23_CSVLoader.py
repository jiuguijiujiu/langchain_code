# 0. 导包
from langchain_community.document_loaders import CSVLoader

# 1. 创建CSV加载器
loader = CSVLoader(
    file_path="./数据/stu.csv",                              # 文件路径
    csv_args={                                              # CSV文件相关参数
        "delimiter": ",",                                       # 分隔符
        "quotechar": '"',                                       # 包围带有分隔符文本的引号是单引号还是双引号
        # "fieldnames": ['name', 'age', 'gender', '爱好']          # 设置表头，如果数据原本有表头，就不要用这代码，如果没有可以使用
    },
    encoding="utf-8"                                        # 设置编码
)

# 2. 一次性加载 .load()   ->  [Document, Document, ...]
# documents = loader.load()
# for document in documents:
#     print(type(document), document)

# 3. 懒加载 .lazy_load()  迭代器[Document]
for document in loader.lazy_load():
    print(type(document), document)