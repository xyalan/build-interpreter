#coding=utf-8
from envir import c_shell
import logging
import os

class Lang:
    def __init__(self, build_config):
        self.build_config = build_config

    def run(self):
        pass

class Java:
    def __init__(self, build_config):
        self.build_config = build_config
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(self.__class__.__name__)

    def set_env(self):
        jdk = ['oraclejdk8']
        jdk = self.build_config['jdk']
        self.log.info("switch use %s", jdk[0])
        c_shell.set_env(JAVA_HOME='/Library/Java/JavaVirtualMachines/jdk1.8.0_91.jdk/Contents/Home')

    def default_script(self):
        if os.path.isfile('pom.xml'):
            return ['mvn', 'clean', 'install']
        elif os.path.isfile('build.gradle'):
            if os.path.isfile('gradlew'):
                return ['./gradlew', 'assemble']
            return ['gradle', 'assemble']

    def install(self):
        script = self.default_script()
        if dict(self.build_config).has_key('script'):
            script = self.build_config['script']
            if isinstance(script, list):
                cus_script = []
                for sc in list(script):
                    cus_script.append(str(sc).split(' '))
                script = cus_script
        # if script == None:
        #     if test:
        #         command = ['mvn', 'clean', 'install', '-Dmaven.test.skip=true']

        self.log.info("execute command %s", script)
        c_shell.exec_cmd(script)

    def run(self):
        self.set_env()
        self.install()



