##�򵥵Ķ��߳�ģ��
import threading
    


semap = threading.Semaphore(200) ##�����߳�������
def semap_run(func,t):   ## ("func",(arg1,arg2)
    with semap:
        threading.Thread(target=func,args=t).start()
    
