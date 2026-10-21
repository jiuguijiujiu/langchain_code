# 0. 导包
import time
import streamlit as st
import config_data as config
from rag import RagService

# 1. 添加网页标题标题
st.title(body="智能客服")
st.divider()                # 分隔符

# 2. 创建消息存储空间
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

# 3. 创建RagService对象
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 4. 循环加载聊天信息，让聊天信息常驻网页
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 5. 在页面最下方提供用户输入栏
prompt = st.chat_input()

# 6. 用户输入聊天信息后的操作
if prompt:
    # 6.1 在聊天页面展示用户的提问，并存储聊天信息
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 6.2 创建存储AI消息的列表
    ai_res_list = []
    with st.spinner("AI思考中..."):
        time.sleep(1)
        # 6.3 用stream方法调用执行链，实现与AI交流的完整流程，返回机器人回答
        res = st.session_state["rag"].chain.stream(input={"input": prompt}, config=config.session_config)

        # 6.4 自定义函数（生成器），实现将AI消息放到AI消息列表里
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                # 6.4.1 防止先攒后输出 的假流式输出，使用yield方法：一个字符一个字符的边存边输出的生成器
                yield chunk

        # 6.5 用write_stream方法，实现AI回复的流式输出
        st.chat_message("assistant").write_stream(capture(res, ai_res_list))    # 因为AI消息接收一次就消失了，所以先存起来，并且防止先攒后输出 的假流式输出，使用yield方法立刻输出
        # 6.6 存储AI回复
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})
        # ["a", "b", "c"]   "".join(list)    -> "abc"
        # ["a", "b", "c"]   ",".join(list)    -> "a,b,c"