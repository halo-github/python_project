#encoding = utf-8
import os 

import base64

def e(s):
    return base64.b64encode(s.encode())

def d(s):
    return base64.b64decode(s).decode()

def bs4_print(s):
    print(e(s))



 
def goto_dir(dir_name):
    if os.path.exists(dir_name) == False:
        os.makedirs(dir_name)
    if os.curdir != dir_name:
        os.chdir(dir_name)

def save_data(name,data,d = os.curdir):
    p = d+"/"+name
    goto_dir(d)
    if os.path.exists(name):
        bs4_print( p, "exists")
        return
    with open(name,'wb') as f:
        f.write(data)
        print(p,"saved")

##"https://www.1010dy.cc/play/62697-1-2/" --> "https://www.1010dy.cc"
def domain_site(url):
    return "/".join(url.split("/")[:3])
