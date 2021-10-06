#coding = utf-8
import threading
import queue
import concurrent.futures as cf

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


def thread_pool(lst,func,args = (),workers = 5):
    ext = cf.ThreadPoolExecutor(max_workers = workers)
    l = [ext.submit(func,i,args) for i in lst]
    # i,arg 分别代表数列的元素，和可能需要的额外参数，所以func的格式应该是两个参数func(i,args)
    return cf.as_completed(l)
