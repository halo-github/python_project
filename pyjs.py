import execjs
from net_lf import net_content
import os
#os.environ["NODE_PATH"] = "node_modules"


js_url = "https://www.1010dy.vip/static/js/player.js?t=a20220403"

player_aaaa={"flag":"play","encrypt":3,"trysee":0,"points":0,"link":"\/play\/62697-1-1\/","link_next":"","link_pre":"\/play\/62697-1-56\/","url":"WWZqYWhubHJOb0duWmdsZlp1RHFraTNhTm5EZ016WVdWaFpXRmlaVGd5TVRjeE1qZzJNREZoTmpOOGFIUjBjSE02THk5M2QzY3ViV2QwZGk1amIyMHZZaTh6T0RBek1ERXZNVEk0TVRJeE9EUXVhSFJ0Ykh3eE5qUTROemsyTmprMg==","url_next":"WWZqYWhubHJOb0duWmdsZlp1RHFraTNhTm5EZ016WVdWaFpXRmlaVGd5TVRjeE1qZzJNREZoTmpOOGZERTJORGczT1RZMk9UWUhtYWNTSEEyNTY=","from":"mgtv","server":"","note":"","id":"62697","sid":1,"nid":57}	

init_str = "new MacPlayer"

test = "function add(a,b){reurn a+b}"
t1 = """
    function pt(c){
        return c + 4;
    }
"""
t2 = """
    function
"""


def js_from(f):
    text = net_content(f)
    str = player_aaaa + "\n" +text + init_str
    return execjs.compile(str)

if __name__ == "__main__":
    #js = js_from(js_url)
    

    ctx = execjs.compile(js_url)
    print(ctx)
    ctx.call("new MacPlayer")
    #c = execjs.get().name
    #print(c)
    #e = ctx.call("pt",aa)
    #a = execjs.eval("5+5")
    #print(e,a)
