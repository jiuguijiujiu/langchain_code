"""
日志工具
"""
# 0. 导包
import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime

# 1. 创建日志保存的根目录
LOG_ROOT = get_abs_path(relative_path="logs")

# 2. 确保日志的目录存在
os.makedirs(name=LOG_ROOT, exist_ok=True)

# 3. 设置日志的格式
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)#  产生日志的时间  logger 的名字   日志等级       产生日志的文件名:产生日志的行号   写的日志内容

# 日志等级排序：DEBUG < INFO < WARNING < ERROR < CRITICAL
# 4. 创建get_logger函数
def get_logger(
        name: str = "agent",                    # logger名称
        console_level: int = logging.INFO,      # 控制台输出日志的最低级别
        file_level: int = logging.DEBUG,        # 写进日志文件的最低级别
        log_file = None,                        # 日志文件的存放路径
) -> logging.Logger:    # 返回日志器对象

    # 4.1 给我一个名字叫 name 的日志器对象，没有就创建一个
    logger = logging.getLogger(name=name)

    # 4.2给这个 logger日志器对象 设一个“等级最低门槛”
    logger.setLevel(level=logging.DEBUG)

    # 4.3 避免重复添加Handler
    # handler 是日志的出口，决定日志输出到哪里
    # 查看handlers是否已经存在，存在则直接返回logger
    # 如果不进行判断，则会重复创建多个出口，那就会重复输出好几次
    if logger.handlers:
        return logger

    # 4.3 创建控制台Handler对象，让日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)                     # 设置控制台输出日志的最低级别
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)            # 设置制台输出日志的格式
    logger.addHandler(console_handler)                          # 将控制台Handler对象挂载到 logger对象上：告诉logger对象，你被调用后，将结果输出到控制台上

    # 4.4 创建日志存放文件的路径
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    # 4.5 创建文件Handler对象，让日志输出到文件里
    file_handler = logging.FileHandler(filename=log_file, encoding='utf-8')
    file_handler.setLevel(file_level)                                   # 设置控制台输出日志的最低级别
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)                       # 设置制台输出日志的格式
    logger.addHandler(file_handler)                                     # 将控制台Handler对象挂载到 logger对象上：告诉logger对象，你被调用后，将结果输出到文件里

    # 4.6 返回日志器对象
    return logger


# 5. 快捷获取日志器
logger = get_logger()

# 6. 测试
# 日志等级排序：DEBUG < INFO < WARNING < ERROR < CRITICAL
if __name__ == '__main__':
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.info("信息日志")
    logger.debug("调试日志")
