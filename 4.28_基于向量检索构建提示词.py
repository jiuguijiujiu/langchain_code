"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
# 0. 导包
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.output_parsers import StrOutputParser

# 1. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 2. 创建提示词模板对象
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问：{input}")
    ]
)

# 3. 创建短期向量存储对象
vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4")
)

# 4. 快速将文本 存储到 向量存储对象中
vector_store.add_texts(
    # 被添加的类型：list[str]
    texts = ["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"]
)

# 5. 准备注入变量的内容
input_text = "怎么减肥？"

# 5.1 检索向量库
result = vector_store.similarity_search(
    query=input_text,
    k=2
)

reference_text = "["
for doc in result:
    reference_text += doc.page_content
reference_text += "]"

# 6. 自定义函数，输出提示词模板
def print_prompt(prompt):
    print(prompt.to_string())
    print("=" * 20)
    return prompt

# 7. 创建链
chain = prompt | print_prompt | model | StrOutputParser()

# 8. 使用invoke方法调用chain
res = chain.invoke({"input": input_text, "context": reference_text})
print(res)