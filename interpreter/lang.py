#coding=utf-8
from envir import c_shell
import logging
import os

class Lang(object):
    def __init__(self, build_config):
        self.build_config = build_config

    def set_env(self):
        if dict(self.build_config).has_key('env'):
            en = self.build_config['env']
            if isinstance(en, str):
                kv = en.split('=')
                c_shell.set_env(**{kv[0]: kv[1]})
            elif isinstance(en, list):
                all_en = {}
                for e in en:
                    kv = e.split('=')
                    all_en[kv[0]] = kv[1]
                c_shell.set_env(**all_en)
    def cus_script(self):
        if dict(self.build_config).has_key('script'):
            script = self.build_config['script']
            if isinstance(script, list):
                cus_script = []
                for sc in list(script):
                    cus_script.append(str(sc).split(' '))
                return cus_script
            return script
        return None

class Java(Lang):
    def __init__(self, build_config):
        super(Java, self).__init__(build_config)
        self.build_config = build_config
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(self.__class__.__name__)

    def set_dk(self):
        if dict(self.build_config).has_key('jdk'):
            jdk = dict(self.build_config).get('jdk')
            self.log.info("switch use %s", jdk)
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
        cus_script = self.cus_script()
        if cus_script is not None:
            script = cus_script
        # if script == None:
        #     if test:
        #         command = ['mvn', 'clean', 'install', '-Dmaven.test.skip=true']
        result = c_shell.exec_cmd(script)
        if not all([e == 0 for e in result]):
            raise Exception("execute error, exit")
    def run(self):
        self.set_dk()
        self.set_env()
        self.install()

class Scala(Lang):
    def __init__(self, build_config):
        super(Scala, self).__init__(build_config)
        self.build_config = build_config
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(self.__class__.__name__)

    def default_script(self):
        if os.path.isfile('build.sbt'):
            return ['sbt', 'clean', 'test']

    def install(self):
        script = self.default_script()
        cus_script = self.cus_script()
        if cus_script is not None:
            script = cus_script

        result = c_shell.exec_cmd(script)
        if not all([e == 0 for e in result]):
            raise Exception("error to execute script, exit")

    def run(self):
        self.set_env()
        self.install()



