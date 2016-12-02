#coding=utf-8
from docker import Client
import time
import logging
from envir import config
import ast
import re

log = logging.getLogger(__name__)

class DockerOpt:
    def __init__(self):
        app_config = config.read_app_config()
        self.app = app_config
        self.url = app_config['docker']['url']
        log.info("create docker with %s", self.url)

    def gen_tag(self, branch, app_version, api_version):
        now = time.localtime()
        now_str = time.strftime("%Y%m%d%H%M%S", now)
        if str(branch).startswith("develop"):
            tag_name = api_version + "-" + app_version + "-d" + now_str
        elif str(branch).startswith("feature/"):
            tag_name = api_version + "-" + app_version + "-f" + now_str
        elif str(branch).startswith("release/"):
            tag_name = api_version + "-" + app_version + "-r" + now_str
        elif str(branch).startswith("hotfix/"):
            tag_name = api_version + "-" + app_version + "-h" + now_str
        else:
            raise Exception('unsupported branch')

        return tag_name

    def gen_repository(self, registry, project_key, app_name):
        return str(registry) + "/" + str(project_key) + "/" + str(app_name)

    def build(self, path, tag):
        """
        Similar to the `docker interpreter`, interpreter a docker image
        :param path: context path include Dockerfile
        :param tag: image's tag
        :return: None
        """
        self.read_port()
        version = self.app['docker']['api']['version']
        cli = Client(base_url=self.url, version=str(version))
        response = cli.build(path, tag)
        for line in response:
            rp = {key: str(item.strip().decode('unicode_escape')) for key, item in ast.literal_eval(line).items()}
            log.info(rp)
        log.info("successful build image with dockerImageTag=%s", str(tag).split(':')[1])

    def push_images(self, repository, tag=None):
        version = self.app['docker']['api']['version']
        cli = Client(base_url=self.url, version=str(version))
        response = cli.push(repository, tag=tag, stream=True)
        for line in response:
            log.info(line)

    def read_port(self):
        with open('Dockerfile') as s:
            con = s.read()
            m = re.search('EXPOSE\s(.+)', con)
            if m:
                port = m.group(1)
                ports = ','.join(port.split(' '))
                log.info('read portsSymbol=%s', ports)
            else:
                raise Exception('Docker file not exists')

    def rm_image(self, repo):
        version = self.app['docker']['api']['version']
        cli = Client(base_url=self.url, version=str(version))
        cli.remove_image(repo)