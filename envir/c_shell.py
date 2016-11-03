# coding=utf-8
import subprocess
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def exec_cmd(cmd):
    if isinstance(cmd, list) and all(isinstance(i, list) for i in list(cmd)):
        result = []
        for c in list(cmd):
            log.info(" ".join(c))
            result.append(subprocess.call(c))
        return result
    elif isinstance(cmd, str):
        cs = cmd.strip().split(' ')
        return [subprocess.call(cs)]
    else:
        raise Exception("命令格式不正确")

def set_env(**kwargs):
    log.info("set env %s", kwargs)
    for k, v in kwargs.iteritems():
        os.environ[k] = v

def subprocess_cmd(command):
    """
    可执行多条命令，多条命令用[;]隔开
    :param command: 需要执行的命令
    :return:
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    proc_stdout = process.communicate()[0].strip()
    log.info(proc_stdout)


