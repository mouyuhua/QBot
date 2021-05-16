import os


def get_function_list():
    """
    返回function目录下的文件列表
    """
    file_path = os.path.dirname(__file__) + '/functions/functions.txt'
    # file_list = os.listdir(file_path)
    if not os.path.exists(file_path):
        return 'ERROR'
    with open(file_path, 'r', encoding='utf-8') as fp:
        return fp.read()


def function_content(name, content):
    """
    获取某个功能的相关描述以及功能概述，需要传入功能名称以及想要获取的内容
    如果没有该功能或者功能描述则返回 ERROR
    参数：name
         content
    """
    file_path = os.path.dirname(__file__) + f'/functions/{name}'
    content_name = content + '.txt'
    if not os.path.exists(file_path):
        return 'ERROR'
    file_list = os.listdir(file_path)
    if content_name not in file_list:
        return 'ERROR'
    with open(file_path+'/'+content_name, 'r', encoding='utf-8') as fp:
        dis = fp.read()
        return dis
