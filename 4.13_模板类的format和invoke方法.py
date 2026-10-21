# 0. 导包
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi

"""
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate  -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate  -> RunnableSerializable -> Runnable
Tongyi -> BaseLLM -> BaseLanguageModel -> RunnableSerializable -> Runnable
ChatTongyi -> BaseChatModel -> BaseLanguageModel -> RunnableSerializable -> Runnable
"""

# 1. 创建通用提示词模板（zero_shot）
template = PromptTemplate.from_template("我的邻居是：{lastname}，最喜欢：{hobby}")

# 2. 使用format方法注入变量
res = template.format(lastname="张大明", hobby="钓鱼")
print(res, type(res))

# 3. 使用invoke方法注入变量
res2 = template.invoke(input = {"lastname": "周杰轮", "hobby": "唱歌"})
print(res2, type(res2))