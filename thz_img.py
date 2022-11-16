#coding:utf-8
import re
import requests
import os
from net_lf import *
from queue_lf import thread_pool
import json
import time
import bs64

from os_lf import *
import threading
json_file = "thz.json"
uu = json.load(open(json_file,'r'))
url_thz = uu["thz"]
url_24 = uu["u24"]

suf_zipai = "forum-42-1.html"
suf_wum = "forum.php?mod=forumdisplay&fid=39&filter=typeid&typeid=1"
page_para_wum =  "<a href=\"([^\"].*)\" .*class=\"s xst\">([^<>].*)</a>"
#page_para_taotu = "<a href=\"(thread.*html)\" .*class=\"s xst\">([^<>].*)</a>"  #资源列表的正则
page_para_zipai = "<a href=\"(thread.*html)\"  onclick.*title=\"(.*)\" class=\"z"  #资源列表的正则
#file="https://www.nsaimg.com/2020/05/26/9be4dd9950c2d.jpg

file_para = "file=\"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"



              # 'thread-2187500-1-1.html
pic_dir = 'D:/xld/thz_pic/'                        #图片储存目录

#获取重定向之后的主页
def real_home_thz():
    r = requests.get("https://user.seven301.xyz:8899/?u=" +url_thz +"/&p=/")
    home = r.url  #http://91thz.cc/forum.php
    l1 = home.split("/")[:-1]
    s1 = "/".join(l1) + "/"
    #print(s1)
    return s1

def real_home_24():
    url = ""
    if os.path.exists(json_file):
        with open(json_file,"rb") as f:
            #print(json.load(f))
            d = json.load(f)
            url = d["u24"]
    else    :
        url = url_24
    #print(requests.get(url).url)
    return requests.get(url).url

home_thz = real_home_thz()
home_24 = real_home_24()




d_thz_zip = {
    "from" : "thz",
    "home" : home_thz,
    "type" : 1,
    "suf" : "forum-42-1.html",
    "tag_name1" : "a",
    "attr1" : {"onclick":"atarget(this)","class":False},#class不能有
    "source1" : "href",
    "tag_name2" : "img",
    "attr2" : {"class" : "zoom"},
    "source2" : "file",
    "dir" : "D:\/xld\/thz_pic/zip"
        }

d_thz_wum = {
    "from" : "thz",
    "home" : home_thz,
    "type" : 2,
    "suf" : "forum.php?mod=forumdisplay&fid=39&filter=typeid&typeid=1",
    "tag_name1" : "a",
    "attr1" : {"class":"s xst"},
    "source1" : "href",
    "tag_name2" : "img",
    "attr2" : {"class" : "zoom","atl":False},
    "source2" : "file",
    "dir" : "D:/xld/thz_pic/wum"

        }

d_24_zip = {
    "from" : "24",
    "home" : home_24,
    "type" : 1,
    "suf" : "thread.php?fid=15",
    "tag_name1" : "a",
    "source1": "href",
    "attr1" : {"href":re.compile("html*"),"id":re.compile("a_aja*")},
    "tag_name2" : "img",
    "attr2" : {"border" : "0"},
    "source2": "src",
    "dir" : "D:\/xld\/24_pic/zip"
        }

d_24_hej = {
    "from" : "24",
    "type" : 2,
    "home" : home_24,
    "suf" : "thread.php?fid=3&type=2",
    "tag_name1" : "a",
    "source1": "href",
    "attr1" : {"href":re.compile("html*"),"id":re.compile("a_aja*")},
    "tag_name2" : "img",
    "attr2" : {"border" : "0"},
    "source2": "src",
    "dir" : "D:\/xld\/24_pic\/hej"
        }
d = d_24_hej



def get_page_list(dic):
    resourse_url = dic["home"] + dic["suf"]
    #print(resourse_url)
    sp = btfsoup(resourse_url)
    lst = sp.find_all(name = dic["tag_name1"], attrs = dic["attr1"])
    lst1 = [(dic["home"] + i.get(dic["source1"]),dic['dir'] + "/" + re.sub(r'[/\?*<>: ]','_',i.string))  for i in lst ]
    
    #print(list(filter(None,lst1)))
    #"https://q227p.cc/pw/"

    return list(filter(None,lst1))



def get_pic_list1(tp,a):
    lst0 = []
    page_url = tp[0]
    save_dir = tp[1]
    #if page_url.startswith("http"):
    try: 
        sp = btfsoup(page_url)     
        lst = sp.find_all(name = d["tag_name2"], attrs = d["attr2"])
        lst1 = [i.get(d["source2"])  for i in lst if i.get(d["source2"]).startswith("http")]
        #print(lst1)
        if len(lst1)>0:
            return (save_dir,lst1)
    except Exception as e:
        print(e)
    finally:
        pass


def down_pic_list(lst):
    for i in lst:
        t1 = time.time()
        r = i.result()
        if r:
            save_dir = r[0]
            lst = r[1]
            #print(r)
            end = thread_pool(lst,down_pic,save_dir)
        t2 = time.time()
        print(t2-t1)




def down_pic(pic_url,save_dir):
    name = os.path.basename(pic_url)
    net_download(pic_url,name,save_dir,True)
    #print(save_dir+name,"saved")



def get_pic_list(page_lst):
    tp_lst = []
    for item in page_lst:
        page_url = item[0]
        save_dir = item[1]
        
        if page_url.startswith("http"):
            sp = btfsoup(page_url)
            if sp != None:
                #print(type(sp))
            
                lst = sp.find_all(name = d["tag_name2"], attrs = d["attr2"])
                #lst1 = filter([],lst)
                lst1 = [i.get(d["source2"])  for i in lst if i.get(d["source2"]).startswith("http")]
                
                #print(len(lst1),page_url,bs64.e(save_dir))
                if len(lst1)>0:
                    #goto_dir(save_dir)
                    #thread_pool(lst1,download_pic,save_dir,workers = 10)
                    #print(page_url)
                    tp_lst.append((save_dir,lst1))
    return tp_lst

def update_url():
    d = {}
    with open(u24,'r') as f:
        d  = json.load(f)
        d["u24"] = home_24
    print(d)
    with open(u24,'w') as f: 
        json.dump(d,f,ensure_ascii=False)

        


if __name__ == '__main__':
    pg_lst = get_page_list(d)
    #print(pg_lst)
    #update_url()
    pic_lst = thread_pool(pg_lst,get_pic_list1,workers = 10)
    print(pic_lst)
    down_pic_list(pic_lst)

