# 0. 导包
import time
import streamlit as st
from agent.react_agent import ReactAgent

# 1. 创建标题
st.title("智扫通机器人智能客服")
st.divider()

# 2. 创建agent对象
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 3. 保存聊天信息
if "message" not in st.session_state:
    st.session_state["message"] = []

# 4. 循环输出聊天信息
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 5. 用户输入问题
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):

            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()