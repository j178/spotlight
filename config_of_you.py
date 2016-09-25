from os.path import dirname, join

# REMEMBER TO CHANGE THIS FILENAME TO config.py

# weibo app
CLIENT_ID = 'your client id'
CLIENT_SECRET = 'your client secret'

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
TURING_KEY = 'your turing key'