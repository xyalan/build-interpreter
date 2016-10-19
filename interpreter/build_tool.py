# encoding=utf-8

class BuildTool:
    def __init__(self, path):
        self.path = path

    def install(self):
        print("Start install dependency")

    def script(self, command):
        print("Start execute interpreter script")