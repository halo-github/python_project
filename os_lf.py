#encoding = utf-8
import os 

def goto_dir(dir_name):
    if os.path.exists(dir_name) == False:
        os.makedirs(dir_name)
    if os.curdir != dir_name:
        os.chdir(dir_name)

def save_data(name,data,d = os.curdir):
    goto_dir(d)
    with open(name,'wb') as f:
        f.write(data)
