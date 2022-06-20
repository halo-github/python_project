import re
from bs4 import BeautifulSoup as soup
from net_lf import net_content,net_group
from os_lf import domain_site,save_data
from queue_lf import thread_pool
#url = "https://www.hobiao.net/vodplay/911043-1-21/"
url = "https://www.1010dy.vip/detail/62697/"
head = domain_site(url)


def doc(r):
    return r.text

def site_list(sp,key_word):
    l1 =  list(i.get("href") for i in sp.find_all(href=re.compile(key_word)))
    all_url =  [head + i for i in l1 ]
    return all_url

def get_aaaa(url,a):
    lst = net_group(url,r'var (player_aaaa={[^}].*})</script><script type="text/javascript" src="([^"]*)"></script><script type="text/javascript" src="([^"]*)"')
    print(lst[0][0],head + lst[0][1], head + lst[0][2])


if __name__ == "__main__":
    text = net_content(url,doc)
    s = soup(text,features="lxml")
    print(s.title)

    #print(s.body)
    #print(s.head)
    
    #按标签索引
    #print(s.head.find_all("meta"))

    #某个节点的全部子节点，不含孙节点，返回list
    #print(len(s.body.contents))
    
    #children也可以用来遍历子节点 类型为list_iterator
    #for i in s.body.children:
    #    print(i)
    
    #全部子孙节点
    #print(list(s.descendants))
    #string只显示第一个,多了显示None，strings可以用来遍历
    #for i in s.body.strings:
    #    print(i)
    #父节点
    #print(s.head.meta.parent.name)
    #兄弟节点
    #print(s.head.prettify)

    #find_all可以用函数作参数
    def has_href(tag) :   
        return tag.has_attr("href")

        #<a href="http://example.com/">I linked to <i>example.com</i></a>
    #print(s.body.select('a[href]'))

    #逐层查找
    #print(s.select('body li a'))
    #ll = [i.get["href"] for i in s.body.find_all("a")]
    #print(ll)
#指定关键字再配合正则，通过get提取
    url_lst = site_list(s,'play')
    thread_pool(url_lst,get_aaaa)
    """print(url_lst)
    #print(s.find_all('script'))
    #return full_url_lst
    with open("1.txt",'w') as f:
        for url in url_lst:
            f.write(url+"\n")
            """
