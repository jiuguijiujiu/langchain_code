# 0. 导包
from langchain_community.document_loaders import JSONLoader

# 1. 创建JSON加载器
loader = JSONLoader(
    file_path="./数据/stu_json_lines.json",            # 文件路径，必填
    jq_schema=".name",                                 # jq解析语法，必填
    text_content=False,     # 告知JSONLoader 我通过 jq_schema 提取的内容不是字符串，不要尝试把它强制转换成字符串，默认True，非必填
    json_lines=True         # 告知JSONLoader 这是一个JSONLines文件，默认False，非必填
)

# 2. 使用load方法调用JSON加载器
documents = loader.load()
print(documents)