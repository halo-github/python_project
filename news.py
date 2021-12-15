from net_lf import *
import json
import jieba.analyse
from collections import Counter
url_ifeng = "https://news.ifeng.com/shanklist/"
idx_ifeng =  ["1","3","5"]

url_xinhua = "http://www.xinhuanet.com/"
ext_xinhua = ["fortunepro","politicspro","techpro"]

url_sina = ["https://finance.sina.com.cn/","https://tech.sina.com.cn/"]


def ifeng():
    d_list = []
    reg = 'var allData = ({.*})'
    for s in idx_ifeng :
        data = net_group(url_ifeng+s,reg)
        js = data[0]
        dic = json.loads(js)
        lst = dic["mainData"]
        lst1 = [i["data"] for i in lst]
        lst2 = [(e["url"],e["title"],e["summary"] if "sunmmary" in e else "") for d in lst1 for e in d] ##二维数组降维
        #print(lst2)
        #print(len(lst2))
        d_list += lst2

    data_list = [(l[0],l[1]) for l in d_list]
    #print(data_list)
    return data_list
    """
    #lst2 = [(d["title"]) for d in e in lst]
    reg = "title\":\"([^\"]+)\",\"url\":\"([^\"]+)"
    s = net_group(url_ifeng1,reg)
    print(s)
    print(len(s))
    """

def xinhua():
    data_list = []
    reg = "<a href=\"([^\"]+)\" target=\"_blank\">([^<\n]{10,})</a>"
    for s in ext_xinhua:
        lst = net_group(url_xinhua+s,reg)
        data_list+=lst
    #print(data_list)
    return data_list

def sina():
    data_list = []
    #<a href="" target="_blank">()</a>
    reg = "<a href=\"([^\"]+)\" target=\"_blank\">([^<]{12,})</a>"
    for s in url_sina:
        lst = net_group(s,reg)
        data_list+=lst
    #print(data_list)
    return data_list


if __name__ == "__main__":
  news_lst = ifeng() + xinhua() + sina()
  analyse_lst = map(lambda x: jieba.analyse.extract_tags(x),[i[1] for i in news_lst]) #jieba词频
  keyword_lst =[e for i in analyse_lst for e in i ]    # 降维
  count = Counter(keyword_lst)
  print(count)
