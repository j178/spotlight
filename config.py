from os.path import dirname, join

# weibo app
CLIENT_ID = '186219443'
CLIENT_SECRET = '32257e2b42c40a6b834e1ad8265334c6'

# filename
ROOT = dirname(__file__)
WEIBO_TOKEN_FILE = join(ROOT, 'data/token.json')
SINCE_ID_FILE = join(ROOT, 'data/since_id.json')

# url
REDIRECT_URI = 'https://my.nigel.top/weibo/auth'
AUTHORIZATION_URL = 'https://api.weibo.com/oauth2/authorize'
ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'

# turing robot
TURING_URL = 'http://www.tuling123.com/openapi/api'
TURING_KEY = '08ad04b298923b29a203d0aca21a9779'
