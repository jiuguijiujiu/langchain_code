# md5
md5_path = "./md5.text"


# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"


# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000        # 文本分割的阈值

# retriever
top_k = 1            # 检索匹配数

# models
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3.7-max"

# session_config
session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
