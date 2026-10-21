# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 创建聊天提示词模板对象
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗"),
    ]
)

# 2. 准备要注入的提示词
history_data = [
    ("human", "你来写一个唐诗"),
    ("ai", "床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午，汗滴禾下锄，谁知盘中餐，粒粒皆辛苦"),
]

# 3. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 4. 创建链，要求每一个组件都是Runnable接口的子类
chain = chat_prompt_template | model

# 5. 通过invoke方法调用链
# res = chain.invoke({"history": history_data})
# print(res.content)

# 6. 通过stream方法调用链
for chunk in chain.stream(input = {"history": history_data}):
    print(chunk.content, end="", flush=True)