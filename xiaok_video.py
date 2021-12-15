#encoding = utf-8
from net_lf import *
from os_lf import goto_dir, save_data
import time
import os
import threading
from queue_lf import thread_pool

video_dir = "E:/xiaok" 
v1 = "https://www.zhihu.com/api/v4/members/huo-huo-95-32/zvideos?offset=0&limit=20&similar_aggregation=true&include=similar_zvideo"

#json解析获取相关数据
def page(r):
    dic = r.json()
    l = dic["data"]
    l1 = [(d["published_at"],d["title"],d["video"]["playlist"]["hd"]["format"],d["video"]["playlist"]["hd"]["play_url"])  for d in l]
    return (l1,dic["paging"])

#while循环获取全部视频地址
def video_list(url,is_end = False):
    v_list = []
    while is_end == False:
        (l,pg) = net_get(url,page,1)
        v_list+=l
        is_end = pg["is_end"]
        url = pg["next"]
    else:
        return v_list


def content(r):
    return r.content




def save_video(tp,a):
    (published_at,title,formt,url) = tp
    name = title + "." + formt
    new_name =str(published_at) + "_" +name
    #return
    if not os.path.exists(new_name):
        print(new_name,threading.current_thread())
        data = net_get(url,content,True)
        save_data(new_name,data,video_dir) 
    else:
        print(new_name + " exist")





if __name__ == "__main__":
    t1 = time.time()
    l = video_list(v1,False)
    #for i in l:
    #    print(i[0])
#多线程下载:
    thread_pool(l,save_video,workers = 8)
