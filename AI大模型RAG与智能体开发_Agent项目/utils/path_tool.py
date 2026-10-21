"""
输出项目中某个文件的绝对路径
"""

# 0. 导包
import os

# 1. 自定义函数，得到项目的绝对路径
def get_project_root() -> str:
    """
    :return: 项目绝对路径字符串
    """
    # 1.1 获取当前这个 Python 文件的绝对路径，保存到 current_file 变量里
    current_file = os.path.abspath(path=__file__)
    # 1.2 获取这个文件的父目录
    current_dir = os.path.dirname(p=current_file)
    # 1.3 再次获取父目录，得到项目的绝对路径
    project_root = os.path.dirname(p=current_dir)
    # 1.4 返回项目绝对路径
    return project_root

# 2. 自定义函数，得到项目中某个文件的绝对路径
def get_abs_path(relative_path: str) -> str:
    """
    输入文件相对路径，返回文件绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    # 1. 得到项目绝对路径
    project_root = get_project_root()
    # 2. 将项目绝对路径 与 项目中文件的相对路径 拼接，得到文件绝对路径，并返回
    return os.path.join(project_root, relative_path)

# 3. 测试
if __name__ == '__main__':
    print(get_abs_path("utils\\path_tool.py"))
