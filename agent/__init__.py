from .cm import ConnectionManger
from .config import MASTER_URL, MYID_PATH
from .msg import Message


class Agent:
    def __init__(self):
        self.message = Message(MYID_PATH)
        self.cm = ConnectionManger(MASTER_URL, self.message)

    def start(self):
        self.cm.start()

    def shutdown(self):
        self.cm.shutdown()
