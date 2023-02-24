#coding:gbk
import re
import requests
import os
from net_lf import *
from queue_lf import thread_pool
import json
import time

from bs4 import BeautifulSoup as soup
from os_lf import *
import threading
json_file = "t24.json"
data = json.load(open(json_file,encoding = "gbk"))


file_para = "file=\"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"




#获取重定向之后的主页
def real_home_thz():
    r = requests.get("https://user.seven301.xyz:8899/?u=" +data["thz"] +"/&p=/")
    home = r.url  #http://91thz.cc/forum.php
    home = http_loc(home)
    return home

def real_home_24():
    url = ""
    if os.path.exists(json_file):
        with open(json_file,"rb") as f:
            d = json.load(f)
            url = data["u24"]
    else    :
        url = url_24
    return requests.get(url).url

home_thz = real_home_thz() + "/"
home_24 = real_home_24()






d = data["d_thz_hej"]




#该函数已验证

def get_page_list(dic):
    if dic["from"] == "24":
        home = home_24
    else:
        home = home_thz
    resourse_url = home + dic["suf"]
    print(resourse_url)
    sp = btfsoup(resourse_url)
    if sp == None: 
        print("get_page_list:None")
        return
    ats = {}
    if dic["attr_type"] == 1:
        ats = dic["attr1"]
    else: 
        ats = eval(json.loads(json.dumps( dic["attr1"])))
    #print(ats)
    #由于json.decoder.JSONDecodeError: Expecting value: line 1 column 9 (char 8)，json字符串需要重新用dumps编码再loads解码才能转换成字典
    #ats1 = eval(json.loads(json.dumps(ats)))  
    #print(repr(ats1))
    #print(type(ats1)) #<class 'dict'>
    lst = sp.find_all(name = dic["tag_name1"], attrs = ats)
    lst1 = [(home  + i.get(dic["source1"]),dic['dir'] + "/" + re.sub(r'[/\?*<>: ]','_',i.string))  for i in lst ]
    
    #print(lst1)
    return list(filter(None,lst1))



def check(tag):
    r1 = d["tag3_lst"][1]
    r2 = d["tag3_lst"][3]

    if tag.name == d["tag3_lst"][0]:
        return tag[r1]
    else:
        return tag[r2]

def has_http(s):
    return s.startswith("http")

def pic_list(sp):
    lst1 = []
    lst11 = []
    lst2 = []
    lst22 = []
    
    if d["type"] == 1:
        lst = sp.find_all(name = d["tag_name2"], attrs = d["attr2"])
        lst1 = [i.get(d["source2"])  for i in lst]
        lst11 = filter(None,lst1)
    if d["type"] == 2:
        tag = sp.find(name = d["tag_name2"], attrs = d["attr2"])
        #print(tag)
        lst1 = tag.find_all(d["tag3_lst"][0])
        lst11 = map(lambda x: x[d["tag3_lst"][1]],lst1)
        lst2 = tag.find_all([d["tag3_lst"][0],d["tag3_lst"][2]])
        lst22 = map(check,lst2)
    lst11 = list(filter(has_http,lst11))
    lst22 = list(filter(has_http,lst22))
    lst33 = [i if i.endswith("jpg") else  i+"-------------------------------------" for i in lst22]
    #ss = set(lst11).issubset(set(lst22))
    result = (lst11,lst33)
    print(result)
    return (result)

def get_pic_list(tp,a):
    lst0 = []
    page_url = tp[0]
    save_dir = tp[1]
    print(page_url)
    #if page_url != "https://q227p.cc/pw/html_data/3/2302/6471599.html":return
    try: 
        sp = btfsoup(page_url)  
        (lst11,lst22) = pic_list(sp)
        if not os.path.exists(save_dir) :
            os.makedirs(save_dir)
        if len(lst22)>0:
            os.chdir(save_dir)
            with open("bt.txt","w") as f:
                f.write(str(lst22))
        return (save_dir,lst11)
    except Exception as e:
            print(e)
    finally:
            pass



def down_pic_list(lst):
    for i in lst:
        #t1 = time.time()
        r = i.result()
        if r:
            save_dir = r[0]
            lst = r[1]
            #print(r)
            end = thread_pool(lst,down_pic,save_dir)
        #t2 = time.time()




def down_pic(pic_url,save_dir):
    name = os.path.basename(pic_url)
    net_download(pic_url,name,save_dir,True)
    #print(save_dir+name,"saved")




def update_url():
    d = {}
    with open(json_file,'r') as f:
        d  = json.load(f)
        d["u24"] = home_24
    #print(d)
    with open(json_file,'w') as f: 
        json.dump(d,f,ensure_ascii=False)

        


if __name__ == '__main__':
    #print(data)

    
    pg_lst = get_page_list(d)
    print(pg_lst)
    if pg_lst == None :
        print("没有数据")
        exit(1)
    print(pg_lst)

    update_url()
    pic_lst = thread_pool(pg_lst,get_pic_list,workers = 10)
    down_pic_list(pic_lst)
