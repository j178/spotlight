# Author: John Jiang
# Date  : 2016/8/18
from .weibo import WeiboClient
# 微博前面的步骤都没有问题，只是最后使用access_token的时候有问题，如果放到Header里的话，微博要的格式是Authorization : OAuth2 xxxxx
# 而requests-oauthlib默认是放在头部中的，而提供的格式是Authorization: Bearer xxxx，所以就总是验证失败
# 所以要手动的吧OAuth2Session._client.default_token_palcement设为'query'，这样再add_token的时候就会以uri?access_token=xxx的形式传递token了

# requests-oauthlib中的token，指的是oauthlib.oauth2.rfc6749.tokens.OAuth2Token这个对象，有自动处理token过期的功能
# 实质是dict的子类，可以用一个dict来初始化
# 所以可以将获取到的json格式的token load为一个dict,然后传给OAuth2Token构造一个对象，赋给session.token，这样为自动地为session._client添加上
# token的属性

# 注册一个access_token_response的hook, 这样在获取到token之后，会将requests的response对象传给hook, 这样就可以把json格式的token保存下来


# 微博使用access token访问API有两种方式：
# 1、 直接使用参数，传递参数名为 access_token
#     https://api.weibo.com/2/statuses/public_timeline.json?access_token=abcd
# 2、在header里传递，形式为在header里添加 Authorization:OAuth2空格abcd，这里的abcd假定为Access Token的值，其它接口参数正常传递即可。
# 真他妈奇葩，前面用的都是OAuth2，到最后一步却变成了这样，token都不加密一下，直接放在params或者header中
