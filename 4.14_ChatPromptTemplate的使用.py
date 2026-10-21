# 0. 导包
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 创建chat提示词模板对象
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

# 3. 使用invoke方法注入信息
prompt_text = chat_prompt_template.invoke(input = {"history": history_data}).to_string()
print(prompt_text)

# 4. 创建模型对象
model = ChatTongyi(model="qwen3.7-max")

# 5. 使用invoke方法调用模型
res = model.invoke(input = prompt_text)

# 6. 输出模型回复结果
print(res.content, type(res))