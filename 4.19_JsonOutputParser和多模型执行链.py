# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# 1. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 2. 创建提示词模板对象
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字，"
    "并封装为JSON格式返回给我。要求key是name，value就是你起的名字，请严格遵守格式要求。"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

# 3. 创建输出解析器对象
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 4. 创建链   （AIMessage("{name: 张若曦}")
chain = first_prompt | model | json_parser | second_prompt | model | str_parser

# 5. 使用stream方法调用链
for chunk in chain.stream({"lastname": "张", "gender": "女儿"}):
    print(chunk, end="", flush=True)