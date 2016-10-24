# encoding=utf-8
import subprocess
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(name)s \n%(message)s')
log = logging.getLogger(__name__)

def exec_cmd(cmd):
    if all(isinstance(i, str) for i in list(cmd)):
        log.info(" ".join(cmd))
        return [subprocess.call(cmd)]
    elif all(isinstance(i, list) for i in list(cmd)):
        result = []
        for c in list(cmd):
            log.info(" ".join(c))
            result.append(subprocess.call(c))
        return result



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
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    log.info(proc_stdout)


