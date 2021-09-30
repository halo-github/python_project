# encoding=gbk
import re
import random
import requests
from fake_useragent import UserAgent
import concurrent.futures as cf
from os_lf import *


def proxy_list():
    def text(r):
            r.encoding = r.apparent_encoding
            return r.text

    #h = Html_handler("")
    ranPage = random.randint(0,10)
    url = "http://www.kuaidaili.com/ops/proxylist/"+str(ranPage)+"/"
    reg = r'"IP">([0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}).*\n.*"PORT">([0-9]{,4}).*\n.*\n.*>(HTT.*)<.*\n'
    #reg = "([0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3})"
    list = net_group(url,reg)
    #print(txt)
    #list = re.findall(reg,txt)
    #print(list)
    proxies = []
    for i in list:
    	dic = {}
    	keys = str(i[2]).split(", ")
    	for key in keys:
    		dic[key] = str(i[0])+":"+str(i[1])
    	proxies.append(dic)
    #print(proxies)
    return proxies	




def net_get(url,f,use_proxy = True):
    try:
        r_headers = {"user-agent": UserAgent().random}
        r_proxy = random.choice(p_list) if use_proxy == True else {}
        r = requests.get(url,headers = r_headers, proxies = r_proxy, timeout = 10, )

    except Exception as e:
            print("while handling " + url)
            print(e)
    else:
            if r.status_code == 200:
                return f(r)
    finally:
        pass


def net_group(url,reg):
    def group(r):
            r.encoding = r.apparent_encoding
            t = r.text
            return re.findall(reg,t)
    return net_get(url,group,False)

    
def net_content(url,use_proxy = True):
    def content(r):
        return r.content
    return  net_get(url,content,use_proxy)

def net_download(url,name,save_path = os.curdir,use_proxy = True):
    data = net_content(url,use_proxy)
    if len(data)>0:
        save_data(name,data,save_path)
    else:
        print(name,"can not saved")

def net_list_handler(lst,func,args = (),workers = 5,use_proxy = True):
    ext = cf.ThreadPoolExecutor(max_workers = workers)
    l = [ext.submit(func,i,args) for i in lst]
    return cf.as_completed(l)

p_list = proxy_list() + proxy_list() + proxy_list()


if __name__ == "__main__":
    p = proxy_list()
    print(p)
    print("# encoding=gbk 才能写中文")
