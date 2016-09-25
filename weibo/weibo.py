# Author: John Jiang
# Date  : 2016/8/18
# http://open.weibo.com/wiki/Oauth2/access_token
import json
import logging
from json.decoder import JSONDecodeError

from oauthlib.oauth2.rfc6749.tokens import OAuth2Token
from requests_oauthlib import OAuth2Session

from config import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)14s] [%(levelname)7s] %(message)s')


class TokenNotExistError(Exception):
    pass


class WeiboClient:
    def __init__(self, refresh=False, base_url=None):
        self.session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
        self.session._client.default_token_placement = 'query'
        self.session.register_compliance_hook('access_token_response', self.save_token_hook)
        self.base_url = base_url or 'https://api.weibo.com/2'
        self.api_path = ''
        if refresh:
            self.oauth2()
        else:
            try:
                self.load_token()
            except TokenNotExistError:
                self.oauth2()

    def __getattr__(self, item):
        self.api_path = '%s/%s' % (self.api_path, item)
        log.debug('Appending api_path \'%s\'' % self.api_path)
        return self

    def post(self, data=None, json=None, **kwargs):
        url = self.base_url + self.api_path + '.json'
        self.api_path = ''
        log.debug('Full url is %s' % url)
        if data is not None and kwargs is not None:
            data.update(kwargs)
        else:
            data = data or kwargs

        return self.session.post(url, data, json)

    def get(self, **kwargs):
        url = self.base_url + self.api_path + '.json'
        self.api_path = ''
        return self.session.get(url, params=kwargs)

    def oauth2(self):
        authorization_url, state = self.session.authorization_url(AUTHORIZATION_URL)
        print('Please go here ', authorization_url)

        redirect_response = input('Paste redirect response here: ').strip()
        self.session.fetch_token(ACCESS_TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                 authorization_response=redirect_response)

    @staticmethod
    def save_token_hook(r, filename=WEIBO_TOKEN_FILE):
        log.debug('Saving token from response')
        with open(filename, 'w') as f:
            f.write(r.text)
        return r

    def load_token(self, filename=WEIBO_TOKEN_FILE):
        try:
            with open(WEIBO_TOKEN_FILE, 'r') as f:
                log.debug('Loading token from file %s' % filename)
                token = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            log.error('Token file not exist or file content has been destroyed')
            raise TokenNotExistError
        self.session.token = OAuth2Token(token)
