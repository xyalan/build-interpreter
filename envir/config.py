# coding=utf-8
import sys
import os
import yaml
import logging
from exception.config_excpetion import NoConfigException
import re

log = logging.getLogger(__name__)

def read_argv():
    """
    读取输入参数，包括5个参数，分别是：
    应用版本、应用名、项目、分支和docker hub地址
    :return: 包含上述几个变量的一个dic
    """
    args = sys.argv
    if len(args) < 5:
        raise ValueError("Pls input required arg!")
    config = {}
    config['project_key'] = args[1]
    config['app_name'] = args[2]
    config['app_version'] = args[3]
    config['branch'] = args[4]
    config['docker_registry'] = args[5]
    config['app_path'] = args[6]
    return config


def read_build_define(build_file):
    """
    读取构建定义文件并解析返回
    :param build_file: 构建定义文件的地址
    :return: 构建定文件的dict
    """
    bf = os.path.join(str(build_file), ".sirius.yml")
    if not os.path.isfile(bf):
        raise NoConfigException('build define file not exists')

    with open(bf, 'r') as yml_file:
        try:
            return yaml.load(yml_file)
        except yaml.YAMLError as exc:
            log.error(exc)

def read_app_config():
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.yml")
    if not os.path.isfile(file_path):
        return {'docker': {'url': 'unix://var/run/docker.sock', 'api': {'version': '1.24'}}}
    with open(file_path) as app:
        try:
            return yaml.load(app)
        except Exception as e:
            log.error(e)

def read_api_version():
    if os.path.isfile(".service.yml"):
        with open('.service.yml') as s:
            sy = yaml.load(s)
            return sy['accessPoint']['apiVersion']
    elif os.path.isfile("SERVICE"):
        with open('SERVICE') as s:
            con = s.read()
            m = re.search('API_VERSION=([^\s]+)', con)
            if m:
                return m.group(1)
            else:
                raise Exception('SERVICE file format error')
    else:
        raise NoConfigException('.service.yml or SERVICE not exists')