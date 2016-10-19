from env import config
from interpreter import install
import time

data = config.read_build_define("/Users/niuoo/Work/code-buid/test/.sirius.yml")
print(data['language'])
localtime = time.localtime()
print(time.strftime("%Y%m%d%H%M%S", localtime))