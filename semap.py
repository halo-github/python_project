##简单的多线程模块
import threading
    


semap = threading.Semaphore(200) ##设置线程数上限
def semap_run(func,t):   ## ("func",(arg1,arg2)
    with semap:
        threading.Thread(target=func,args=t).start()
    
