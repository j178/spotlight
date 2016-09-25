from weibo import WeiboClient
from weibo.watchyou import fetch_replies

for r in fetch_replies():  # fetch_replies所依赖的weibo全局变量是在watchyou模块中存在的, 函数无法访问到这个模块中的全局变量
    print(r['text'])
