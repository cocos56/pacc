"""XML文件内容读取模块"""
from html import unescape
from xml.dom import minidom


def get_xml(file_path):
    """从文件中读取xml内容

    :param file_path: 文件路径
    :return: 返回xml文件的原始内容
    """
    return open(file_path, 'r', encoding='utf-8').read()


def get_pretty_xml(file_path):
    """从文件中读取xml内容（以较为美观的形式展现）

    :param file_path: 文件路径
    :return: 返回美化后的xml文件内容
    """
    xml = get_xml(file_path)
    xml = minidom.parseString(xml)
    xml = xml.toprettyxml()
    xml = unescape(xml)
    with open(file_path, 'w', encoding='utf-8') as file_stream:
        file_stream.writelines(xml)
    return xml
