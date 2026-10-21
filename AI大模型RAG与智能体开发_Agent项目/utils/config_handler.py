"""
将yaml文件里的内容转为字典
yaml文件格式：k: v
"""
# 0. 导包
import yaml
from utils.path_tool import get_abs_path

# 1. 创建 将yaml文件里的内容转为字典 的函数
def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)             # 把文件对象里的 YAML 文本，解析成 Python 对象（通常是字典）


def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 2. 调用函数，将yaml文件里的内容转为字典
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()

# 3. 测试
if __name__ == '__main__':
    print(rag_conf["chat_model_name"])
    print(type(rag_conf))
