#coding=utf-8
from envir import config
import logging
import sys
from lang import Java
from lang import Scala
import os

log = logging.getLogger(__name__)

try:
    build_config = config.read_build_define("../test/.sirius.yml")
    input_args = config.read_argv()
except:
    log.error("error to read build file or args")
    sys.exit()


def compile_file():
    lan = build_config['language']


def prepare_env():
    print()

def main():
    lan = str(build_config['language']).lower()
    project_root = input_args['app_path']
    if lan.__contains__('java'):
        os.chdir(project_root)
        java = Java(build_config)
        java.run()
    elif lan.__contains__('scala'):
        os.chdir(project_root)
        scala = Scala(build_config)
        scala.install()
    elif lan.__contains__("javascript"):
        print("use javascript")

if __name__ == "__main__":
    main()
