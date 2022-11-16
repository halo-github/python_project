# encoding=gbk
import re
import random
import requests
from fake_useragent import UserAgent
from os_lf import *
from bs4 import BeautifulSoup as soup




def proxy_list():
    def text(r):
            r.encoding = r.apparent_encoding
            return r.text

    #h = Html_handler("")
    ranPage = random.randint(0,10)
    url = "http://www.kuaidaili.com/ops/proxylist/"+str(ranPage)+"/"
    reg = r'"IP">([0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}).*\n.*"PORT">([0-9]{,4}).*\n.*\n.*>(HTT.*)<.*\n'
    #reg = "([0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3})"
    lst = net_group(url,reg)
    #print(lst)
    #list = re.findall(reg,txt)
    #print(list)
    proxies = []
    for i in lst:
    	dic = {}
    	keys = str(i[2]).split(", ")
    	for key in keys:
    		dic[key] = str(i[0])+":"+str(i[1])
    	proxies.append(dic)
    #print(proxies)
    return proxies	


def redirect_url(url):
    rsp =  requests.get(url)
    return rsp.url

def net_get(url,f,use_proxy = True):
    try:
        requests.packages.urllib3.disable_warnings()
        s = requests.Session()
        s.keep_alive = False
        ##fake_useragent报错：Maximum amount of retries reached，解决方法为在临时文件夹增加一个fake_useragent.json
        
        agent = UserAgent(path="C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\fake_useragent.json")
        r_headers = {"user-agent":str(agent.random)}

        r_proxy = random.choice(p_list) if use_proxy == True else {}
        #print(r_proxy)
        r = requests.get(url,headers = r_headers, proxies = r_proxy, timeout = 5,verify=False)
        #print(r_proxy)
    #可能出现HTTPConnectionPool，但不影响，可以pass
    #except HTTPConnectionPool    :
    #    print("HTTPConnectionPool " + url)        
    except Exception as e:
            print("while handling " + url)
            print(e,url)
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


#BeautifulSoup
def btfsoup(url):
    s = None
    try:
        text = net_content(url)
        if text != None:
            s = soup(text,features="lxml")  ##lxml  html.parser
    except Exception as e:
        print(e)
    finally:
        return s



p_list = proxy_list() + proxy_list() + proxy_list()


if __name__ == "__main__":
    s = "https://q227p.cc/pw/html_data/3/2111/5673146.html"
    sp = btfsoup(s)
    print(type(sp))
    
    #p = p_list
    print(sp)
    #print("# encoding=gbk 才能写中文")
    
