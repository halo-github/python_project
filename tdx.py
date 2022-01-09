#coding = gbk
import os
import struct
import pandas as pd
from queue_lf import thread_pool
xls_dir = "D:\stork\data"
hwx_dir = "D:\Program Files (x86)\hwx\\vipdoc\\"
sh_dir = hwx_dir +"sh\lday"
sz_dir = hwx_dir + "sz\lday"
f1 = 'D:\Program Files (x86)\hwx\\vipdoc\sh\lday\sh000043.day'

to_str = lambda x:str(x)

def dayfile_to_xlsx(f,a):
    #读取day文件
    file = open(f,'rb')
    b = file.read()
    file.close()
    #print(b)
    #下面是解析过程
    empty_list = []
    a = 0
    l = len(b)/32
    for i in range(0,int(l)):
        data = struct.unpack('IIIIIfII',b[a:a+32])
        #print(data[4]/100)
        data1 =[data[0],data[1]/100,data[2]/100,data[3]/100,data[4]/100,data[5]/10,data[6],data[7]] 
        empty_list.append(data1)
        a+=32
    #二维数组转化成DataFrame
    df = pd.DataFrame(empty_list, columns = ["date","open","high","low","close","amount","vol","str7"])

    name = os.path.basename(f).split(".")[0]
    full_path = xls_dir + os.sep + name + ".xlsx"     #这里需要xlsx格式，而不是xls
    print(full_path)
    #存入xlsx文件
    df.to_excel(full_path)


if __name__ == "__main__":
    sh_list = list(map(lambda x: sh_dir + "\\" + x, os.listdir(sh_dir)))
    sz_list = list(map(lambda x: sz_dir + "\\" + x, os.listdir(sz_dir)))
    file_list = sh_list + sz_list
    #print(file_list)
    thread_pool(file_list,dayfile_to_xlsx,workers = 145)

