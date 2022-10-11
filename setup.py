"""安装模块"""
from setuptools import setup, find_packages
from pacc import get_version, get_long_description, get_description

setup(
    name='pacc',  # 包名
    version=get_version(),  # 版本
    packages=find_packages(),  # 目录下所有文件
    description=get_description(),  # 简述信息
    long_description=get_long_description(),  # 详述信息
    author='Coco',  # 作者
    author_email='zj175@139.com',  # 作者邮箱
    url='https://github.com/cocos56/pacc',  # 主页
)
