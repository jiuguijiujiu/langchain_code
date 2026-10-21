# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# 1. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 2. 创建提示词对象
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字，仅生成一个名字，并告知我名字，不要额外信息。"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name}，请帮我解析含义。"
)
# 3. 创建字符串输出解析器
str_parser = StrOutputParser()

# 函数的入参：AIMessage -> dict  ({"name": "xxx"})
# my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# 4. 创建链
chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser

# 5. 使用stream方法调用链
for chunk in chain.stream({"lastname": "曹", "gender": "女孩"}):
    print(chunk, end="", flush=True)