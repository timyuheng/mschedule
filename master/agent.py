from commom.state import *

class Agent:
    def __init__(self, id, hostname, ip):
        self.id = id
        self.hostname = hostname
        self.ip = ip # ip列表
        self.state = WAITING
        self.outputs = {} # 保持不同任务执行结果 {task_id:(code,output)}


    def __repr__(self):
        return "<Agent {} {} {} {}>".format(self.id, self.hostname, self.ip, self.state)


