"""
基于Streamlit完成WEB网页上传服务

pip install streamlit

Streamlit：当WEB页面元素发生变化，则代码重新执行一遍
"""
# 0. 导包
import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 1. 添加网页标题
st.title(body="知识库更新服务")

# 2. 上传文件的入口，file_uploader
uploader_file = st.file_uploader(
    label = "请上传TXT文件",          # 标题
    type=['txt'],                   # 接收文件的类型
    accept_multiple_files=False,    # False表示仅接受一个文件的上传
)

# session_state：长时间存储 streamlit值 的空间，就是一个字典
# 创建知识库对象
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 3. 接收文件后的操作
if uploader_file is not None:
    # 3.1 提取文件的信息
    file_name = uploader_file.name           # 文件名
    file_type = uploader_file.type           # 文件类型
    file_size = uploader_file.size / 1024    # 文件大小，KB

    # 3.2 展示文件信息
    st.subheader(body=f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # 3.2 提取文件内容
    # get_value -> bytes(字节串) -> decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner(text="载入知识库中..."):       # 在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        # 3.3 用upload_by_str方法调用知识库对象存储文件内容
        result = st.session_state["service"].store_knowledge(text=text, file_name=file_name)
        st.write(result)