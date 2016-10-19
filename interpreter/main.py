#coding=utf-8
from env import config
import logging
import sys
from lang import Java
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
    if lan.__contains__('java'):
        os.chdir(input_args['app_path'])
        print build_config
        java = Java(build_config)
        java.run()
    elif lan.__contains__("javascript"):
        print("use javascript")

if __name__ == "__main__":
    main()
