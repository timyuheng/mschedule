import subprocess
from subprocess import Popen
from utils import getlogger
import tempfile

logger = getlogger(__name__, r"F:\Python\code\project\mschedule\log\agent.exec.log")


class Executor:
    def run(self, script, timeout=None):
        '''
        使用script, 运行脚本

        :param script: 脚本
        :param timeout: 超时时间
        :return: (状态码, 输出)
        '''
        with tempfile.TemporaryFile("w+b") as f:
            proc = Popen(script, shell=True, stdout=f, stderr=f)
            try:
                code = proc.wait(timeout)
                f.seek(0)
                if code == 0:
                    txt = f.read()
                else:
                    txt = f.read()

                logger.info("{} {}".format(code, txt))
                return code, txt

            except Exception as e:
                logger.error(e)
                return (1, "") # 有异常也返回状态码和信息


if __name__ == '__main__':
    exec = Executor()
    exec.run("pause", timeout=2)
