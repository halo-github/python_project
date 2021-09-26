#coding = utf-8
import threading
import queue

class Worker(threading.Thread):
    def __init__(self,t_name,queue,func,args):
        super().__init__(name = t_name)
        self.func = func
        self.args = args
        self.queue = queue

    def run(self):
        self.result = self.func(self.args)

    def getResult(self):
        return self.result
