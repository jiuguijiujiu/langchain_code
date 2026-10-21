# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 2. 创建提示词模板对象
prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其它内容。"
)

# 3. 创建字符串输出解析器对象
parser = StrOutputParser()

# 4. 创建链
chain = prompt | model | parser | model | parser

# 5. 使用invoke方法调用链
res = chain.invoke(input = {"lastname": "张", "gender": "女儿"})

# 6. 输出模型回复结果
print(res)
print(type(res))