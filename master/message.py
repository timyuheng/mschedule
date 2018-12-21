from utils import getlogger
from .storage import Storage

logger = getlogger(__name__, r"F:\Python\code\project\mschedule\log\master.msg.log")


class Message:
    '''负责消息处理'''

    def __init__(self):
        self.store = Storage()

    def reg(self, msg):  # 注册接口
        print(msg, type(msg))

        ts = msg['timestamp']
        self.store.reg(msg['id'], msg['hostname'], msg['ip'])
        return "reg {}".format(msg)

    def heartbeat(self, msg):  # 心跳接口
        print(msg, type(msg))

        ts = msg['timestamp']
        self.store.heartbeat(msg['id'], msg['hostname'], msg['ip'])
        return 'hb {}'.format(msg)

    def add_task(self, task: dict):  # json被转成了字典
        return self.store.add_task(task)

    def pull_task(self, agent_id):  # 拉任务接口
        # agnet 空闲就主动领取任务
        # 有任务返回信息. 否则返回None
        # (task.id, task.timeout, task.script)
        # 遍历任务状态是RUNNING或Warting的任务, 其中tagat中tagrat_id是自己的且状态是waiting的
        return self.store.get_task_by_agentid(agent_id)  # 返回了元组或None

    def result(self, msg):
        self.store.result(msg)
        return "ack msg"

    def get_agents(self):
        return self.store.get_agents()
