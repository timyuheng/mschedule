import zerorpc
from .config import MASTER_URL
from .message import Message

class ConnerctionManager:
    def __init__(self):
        self.server = zerorpc.Server(Message())
        self.server.bind(MASTER_URL)

    def start(self):
        self.server.run()

    def shutdown(self):
        self.server.close()





