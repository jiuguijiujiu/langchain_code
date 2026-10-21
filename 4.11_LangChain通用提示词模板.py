# 0. 导包
from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# 1. 创建通用提示词模板对象（zero-shot）
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 你帮我起个名字，简单回答。"
)

# 2. 标准写法
# # 2.1 使用format方法注入信息
# prompt_text = prompt_template.format(lastname="张", gender="女儿")   # 返回的是提示词对象
# # 2.2 创建模型对象
# model = Tongyi(model="qwen-max")
# # 2.3 使用invoke方法调用模型
# res = model.invoke(input=prompt_text)     # 模型对象可以直接接收提示词对象
# # 2.4 返回模型回复结果
# print(res)

# 3. 基于chain链的写法
# 3.1 创建模型对象
model = Tongyi(model="qwen-max")
# 3.2 创建链
chain = prompt_template | model
# 3.3 基于chain链 invoke方法 注入信息到提示词模板
res = chain.invoke(input={"lastname": "张", "gender": "女儿"})
# 3.4 输出模型回复结果
print(res)