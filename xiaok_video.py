#encoding = utf-8
from net_lf import *
from os_lf import goto_dir, save_data
import time
import concurrent.futures as cf
import os
import threading

video_dir = "E:/xiaok" 
v1 = "https://www.zhihu.com/api/v4/members/huo-huo-95-32/zvideos?offset=0&limit=20&similar_aggregation=true&include=similar_zvideo"
def page(r):
    dic = r.json()
    l = dic["data"]
    l1 = [{"t":d["title"],"f":d["video"]["playlist"]["hd"]["format"],"v":d["video"]["playlist"]["hd"]["play_url"]} for d in l]
    return (l1,dic["paging"])

def video_list(url,is_end = False):
    v_list = []
    while is_end == False:
        (l,pg) = net_get(url,page,True)
        v_list+=l
        is_end = pg["is_end"]
        url = pg["next"]
    else:
        return v_list


def content(r):
    return r.content




def save_video(title, formt, url):
    name = title + "." + formt
    if os.path.exists(name):
        print(name + " exist")
        return
    data = net_get(url,content,True)
    save_data(name,data,video_dir)
    print("saved " + video_dir + "/" + name + " in thread: " + str(threading.current_thread()) )
    
def downloader(lst):
        ext = cf.ThreadPoolExecutor(max_workers = 8)
        l = [ext.submit(save_video,d["t"],d["f"],d["v"]) for d in lst]
        for f in cf.as_completed(l):
            print(f.result())





if __name__ == "__main__":
    t1 = time.time()
    l = video_list(v1,False)
    print(len(l))
    t2 = time.time()
    print(t2 - t1)
    downloader(l)
    t3 = time.time()
    print(t3 - t2)


