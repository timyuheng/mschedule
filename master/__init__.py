from .cm import ConnerctionManager

class Master:
    def __init__(self):
        self.cm = ConnerctionManager()

    def start(self):
        self.cm.start()

    def shutdown(self):
        self.cm.shutdown()

