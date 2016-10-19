# encoding=utf-8
import logging
import os

from env import c_shell
from interpreter.build_tool import BuildTool

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class Maven(BuildTool):
    """
    Maven编译工具实现，主要包括安装依赖
    """
    def __init__(self, path):
        BuildTool.__init__(self, path)
        self.path = path
        os.chdir(path)
        log.info("Dir change to %s", os.getcwd())

    def install(self):
        log.info("Dir is %s", os.getcwd())
        # shell.exec_cmd(['mvn', 'install'])

    def script(self, command):
        c_shell.exec_cmd(['mvn', 'clean', 'install'])

mvn = Maven("..")
print mvn.install()

