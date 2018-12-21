from commom.state import *

class Task:
    def __init__(self, id, script, targets, timeout=None, parallel=1, fail_rate=0, fail_count=1):
        self.id = id
        self.script = script
        self.state = WAITING
        self.timeout = timeout # 任务在Agent上执行的超时时长
        self.parallel = parallel # 该任务要同时派给几个Agent跑
        self.fail_rate = fail_rate # 失败率上限，超过则任务执行失败FAILED
        self.fail_count = fail_count  # 失败上限，超过则任务执行失败FAILED
        self.targets = targets # 此任务派发给几个agent执行['id1', 'id2']
        self.targets_count = len(self.targets)

    def __repr__(self):
        return "<Task {}>".format(self.id)
