import zerorpc
import threading
from .msg import Message
from utils import getlogger
from commom.state import *
from threading import Thread
from .executor import Executor

logger = getlogger(__name__, r"F:\Python\code\project\mschedule\log\agent.cm.log")


class ConnectionManger:
    def __init__(self, master_url, message: Message):
        self.master_url = master_url
        self.client = zerorpc.Client()
        self.message = message
        self.event = threading.Event()
        self.state = WAITING

        self.executor = Executor()
        self.__result = None

    def _exec(self, task):
        task_id, task_timeout, task_script = task

        # 执行，超时返回非0状态码
        # TODO：为了测试简单，没有对脚本做base64编码，后期加上
        code, output = self.executor.run(task_script, task_timeout)

        self.__result = task_id, code, output
        self.state = SUCCESSFUL if code == 0 else FAILED

    def start(self, interval=5):
        while not self.event.is_set():  # 支持重连
            try:
                self.client.connect(self.master_url)
                # 注册客户端, 序列化字典
                ack = self.client.reg(self.message.reg())
                logger.info("{}".format(ack))
                # 心跳循环
                while not self.event.wait(interval):
                    ack = self.client.heartbeat(self.message.heartbeat())
                    print(ack)

                    if self.state in {SUCCESSFUL, FAILED}:
                        self.client.result(self.message.result(*self.__result))  # 生成结果
                        self.__result = None  # 用完置空
                        self.state = WAITING

                    if self.state == WAITING:  # 空闲则拉任务
                        task = self.client.pull_task(self.message.id)

                        if task:  # None或(task.id, task.timeout, task.script)
                            self.state = RUNNING  # 获取到任务将状态置为RUN
                            Thread(target=self._exec, args=(task,), name="exectask").start()

            except Exception as e:
                logger.error(e)
                raise e

    def shutdown(self):
        self.event.set()
        self.client.close()

    # def join(self):
    #     self.event.wait()
