#encoding = utf-8
from net_lf import *
from os_lf import goto_dir, save_data
import time
import os
import threading
import pandas as pd
from queue_lf import thread_pool

#idx = input("1,xiaok, 2,天启\n")
excel_dir = "D:\stork\\video_url"
video_dir = "E:/xiaok" 
url_lst = ["https://www.zhihu.com/api/v4/members/lis-10-69/zvideos?offset=0&limit=20&similar_aggregation=true&include=similar_zvideo%2Ccreation_relationship","https://www.zhihu.com/api/v4/members/123bo-yi-xue-yuan-24/zvideos?offset=0&limit=20&similar_aggregation=true&include=similar_zvideo%2Ccreation_relationship", "https://www.zhihu.com/api/v4/members/huo-huo-95-32/zvideos?offset=0&limit=20&similar_aggregation=true&include=similar_zvideo"  ] #天启

author_list = ["天启大烁哥","123博弈财经","小K复盘"]

func = lambda lst: [(d["published_at"],d["author"]["name"],d["title"],d["video"]["playlist"]["sd"]["format"],d["video"]["playlist"]["sd"]["play_url"])  for d in lst] #sd： 标清 hd：高清
#json解析获取相关数据
def page(r):
    dic = r.json()
    l = dic["data"]
    return (func(l),dic["paging"])

#while循环获取全部视频地址
def video_list(url,is_end = False):
    v_list = []
    t = time.time()
    while is_end == False:
        (l,pg) = net_get(url,page)
        v_list+=l
        is_end = pg["is_end"]
        url = pg["next"]
    else:
        name = v_list[0][1]
        print(name + " 单次用时 %.2f秒 "%(time.time()-t1))
        return v_list


def content(r):
    return r.content


def url_to_xlsx(lst):
    #print(lst)
    goto_dir(excel_dir)
    pd.DataFrame().to_excel('url.xlsx')
    #print(lst)
    with pd.ExcelWriter("url.xlsx", mode = "a", engine = "openpyxl") as writer:
            for i in lst:
                df = pd.DataFrame(i,columns = ["published_at","author","tilte","format","url"])
                ky = i[0][1]
                #print(ky)
                df.sort_values("published_at",ascending = False).to_excel(writer,sheet_name = ky)

def save_video(tp,a):
    (published_at,author,title,formt,url) = tp
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
    l = thread_pool(url_lst,video_list,args = False, workers = 10)
    l1 = [i.result() for i in l]
    t2 = time.time()
    choice = input("%.2f秒读取完成\n1，保存视频地址，2，下载视频, 其余退出\n"%(t2-t1))
    if choice == "1":
        url_to_xlsx(l1)
    if choice == "2":
        ipt = input("下载：1，天启大烁哥，2，123博弈财经，3，小K复盘，其余退出\n")
        idx = int(ipt) - 1
        idx_selected = 0
        for i in range(len(l1)):
            print(author_list[idx],l1[i][0][1])
            if author_list[idx] == l1[i][0][1]:
                idx_selected = i
                break
        print(idx_selected)    
        thread_pool(l1[idx_selected],save_video,workers = 8)       #多线程下载
