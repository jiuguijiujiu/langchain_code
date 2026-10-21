# 0. 导包
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from utils.config_handler import prompts_conf

# 1. 创建 加载系统提示词 函数
def load_system_prompts():
    # 1.1 得到 系统提示词存储文件 的绝对路径
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置项中没有main_prompt_path配置项")
        raise e
    # 1.2 返回 系统提示词存储文件内容
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词出错，{str(e)}")
        raise e

# 2. 创建 加载rag提示词 函数
def load_rag_prompts():
    # 2.1 得到 rag提示词存储文件 的绝对路径
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e
    # 2.2 返回 rag提示词存储文件内容
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错，{str(e)}")
        raise e

# 3. 创建 加载报告提示词 函数
def load_report_prompts():
    # 3.1 得到 报告提示词存储文件 的绝对路径
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置项中没有report_prompt_path配置项")
        raise e
    # 3.2 返回 报告提示词存储文件内容
    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告生成提示词出错，{str(e)}")
        raise e

# 4. 测试
if __name__ == '__main__':
    print(load_report_prompts())

