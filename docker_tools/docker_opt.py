#coding=utf-8
from docker import Client
import time
import logging


class DockerOpt:
    def __init__(self, url):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        # sh.setLevel(logging.INFO)
        self.log.addHandler(sh)
        self.log.debug("create docker with %s", url)
        self.url = url

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
        cli = Client(base_url=self.url)
        response = [line for line in cli.build(path, tag)]
        self.log.info(response)

    def push_images(self, repository, tag=None):
        cli = Client(base_url=self.url)
        response = [line for line in cli.push(repository, tag=tag, stream=True)]
        self.log.info(response)