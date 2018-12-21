from .agent import Agent
import uuid
from .task import Task
from commom.state import *


class Storage:
    def __init__(self):
        self.agents = {}
        self.tasks = {}

    def reg(self, id, hostname, ip):
        if id not in self.agents.keys():
            self.agents[id] = Agent(id, hostname, ip)
        else:
            agent = self.agents[id]
            agent.hostname = hostname
            agent.ip = ip

    def heartbeat(self, id, hostname, ip):
        if id not in self.agents.keys():
            self.agents[id] = Agent(id, hostname, ip)

        else:
            agent = self.agents[id]
            agent.hostname = hostname
            agent.ip = ip

    def add_task(self, task: dict):
        id = uuid.uuid4().hex
        t = Task(id, **task)
        t.targets = {agent_id: self.agents[agent_id] for agent_id in t.targets}  # 构建Agent实例字典
        self.tasks[t.id] = t
        return t.id

    def iter_tasks(self, states={WAITING, RUNNING}):
        yield from (task for task in self.tasks.values() if task.state in states)

    def get_task_by_agentid(self, agent_id):
        for task in self.iter_tasks():
            if agent_id in task.targets.keys():
                agent = task.targets[agent_id]
                if task.id not in agent.outputs:  # 没有领取过
                    agent.outputs[task.id] = None

                    agent.state = RUNNING
                    task.state = RUNNING

                    return (task.id, task.timeout, task.script)  # 找到一个任务就返回去执行

    def result(self, msg):
        task = self.tasks[msg['id']]

        task.state = SUCCESSFUL
        agent = task.targets[msg['agent_id']]
        code = msg['code']
        output = msg['output']
        agent.outputs[task.id] = code, output
        agent.state = WAITING  # 又可以接任务了

    def get_agents(self):
        return list(self.agents.keys())
