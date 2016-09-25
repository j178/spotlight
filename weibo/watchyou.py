import time

import requests

from weibo import WeiboClient
from weibo.config import *


def fetch_statuses(uid=None, screen_name=None):
    """
    微博API升级, statuses/user_timeline接口的 uid/screen_name 只能为当前授权的用户, 即与 access_token 的所有者要匹配
    测试使用home_timeline然后筛选是否可以
    :param int uid: uid
    :param str screen_name: 二选一
    """
    since_id = get_since_id()
    params = dict(since_id=since_id, max_id=None, count=100, page=None, trim_user=0)

    first = True
    while True:
        j = weibo.statuses.home_timeline.get(**params).json()
        if first:
            save_since_id(j['since_id'])
            first = False
        spots = list(filter(lambda s: s['user']['screen_name'] == screen_name, j['statuses']))
        if not spots:
            return
        yield from spots
        params['max_id'] = j['max_id']
        time.sleep(5)


def get_since_id():
    try:
        since_id = open(SINCE_ID_FILE).read() or None
    except FileNotFoundError:
        since_id = None
    return since_id


def save_since_id(since_id):
    since_id = str(since_id)
    with open(SINCE_ID_FILE, 'w') as fp:
        fp.write(since_id)


def repost():
    pass


def like():
    pass


def comment(id, text):
    r = weibo.comments.create.post(id=id, comment=text)
    time.sleep(3)


def comment_all(who):
    for s in fetch_statuses(screen_name=who):
        cmt = robot(s['text'])
        comment(s['id'], cmt)
        print(s['screen_name'], s['text'], cmt)


def reply(id, cid, text):
    pass


def robot(info):
    j = requests.post(TURING_URL, json={'key': TURING_KEY, 'info': info}).json()
    return j['text']


if __name__ == '__main__':
    weibo = WeiboClient()

    #     print(s)
    # 取消关注一些账号, 用新买的号或者就是现在用的号
    # 每十分钟刷新一次timeline, 获取他的微博, 并获取私信或者回复消息
    # 调用机器人api, 发表评论, 回复消息
