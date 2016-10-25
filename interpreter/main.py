#coding=utf-8
from envir import config
import logging
import sys
from lang import Java
from lang import Scala
import os
from docker_tools.docker_opt import DockerOpt
from exception.config_excpetion import NoConfigException

log = logging.getLogger(__name__)

try:
    input_args = config.read_argv()
    build_config = config.read_build_define(input_args['app_path'])
except NoConfigException as error:
    log.warning(error)
    build_config = {'language': 'java'}
except Exception as error:
    log.error("error to read build file or args %s", error)
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
    cli = DockerOpt()
    re = cli.gen_repository(input_args['docker_registry'], input_args['project_key'], input_args['app_name'])
    tag = cli.gen_tag(input_args['branch'], input_args['app_version'], '1.0.1')
    image_name = str(re) + ':' + tag
    log.info("build images %s", image_name)
    cli.build('.', image_name)
    log.info("push image %s", image_name)
    cli.push_images(image_name)

if __name__ == "__main__":
    main()
