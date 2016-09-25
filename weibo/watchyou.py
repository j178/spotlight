import json
import time

import requests

from config import *
from weibo import WeiboClient


def fetch_statuses(uid=None, screen_name=None):
    """
    微博API升级, statuses/user_timeline接口的 uid/screen_name 只能为当前授权的用户, 即与 access_token 的所有者要匹配
    测试使用home_timeline然后筛选是否可以
    :param int uid: uid
    :param str screen_name: 二选一
    """
    since_id = get_since_id('status')
    params = dict(since_id=since_id, max_id=None, count=100, page=None, trim_user=0)

    first = True
    while True:
        j = weibo.statuses.home_timeline.get(**params).json()
        if first:
            save_since_id('status', j['since_id'])
            first = False
        spots = list(filter(lambda s: s['user']['screen_name'] == screen_name, j['statuses']))
        if not spots:
            return
        yield from spots
        params['max_id'] = j['max_id']
        time.sleep(5)


def fetch_replies():
    since_id = get_since_id('reply')
    params = dict(since_id=since_id, max_id=None, count=100, page=None, trim_user=0)

    first = True
    while True:
        j = weibo.comments.to_me.get(**params).json()
        comments = j['comments']
        if len(comments) == 0:
            return

        if first:
            save_since_id('reply', comments[0]['id'])
            first = False

        yield from comments
        params['max_id'] = comments[-1]['id'] - 1  # 保证最后一条不再返回
        time.sleep(5)


def get_since_id(type=None, file=SINCE_ID_FILE):
    if type is None:
        return get_since_id.since_id

    if hasattr(get_since_id, 'since_id') and get_since_id.since_id:
        return get_since_id.since_id[type]

    try:
        with open(file) as f:
            get_since_id.since_id = json.load(f)
            return get_since_id.since_id[type]
    except FileNotFoundError:
        return None


def save_since_id(type, since_id):
    with open(SINCE_ID_FILE, 'w') as fp:
        get_since_id()[type] = since_id
        json.dump(get_since_id(), fp)


def repost():
    pass


def like():
    pass


def comment(id, text):
    weibo.comments.create.post(id=id, comment=text)
    time.sleep(3)


def comment_all(who):
    for s in fetch_statuses(screen_name=who):
        cmt = robot(s['text'])
        comment(s['id'], cmt)
        print(s['screen_name'], s['text'], cmt)


def reply(id, cid, text):
    weibo.comments.reply.post(id=id, cid=cid, comment=text)
    time.sleep(3)


def reply_all():
    for r in fetch_replies():
        cmt = r['text'].split(':', 1)  # maxsplit 参数: 最多分几下
        reply(r['status']['id'], r['id'], robot(cmt))
        print(r['text'])


def robot(info):
    j = requests.post(TURING_URL, json={'key': TURING_KEY, 'info': info}).json()
    return j['text']


weibo = WeiboClient()
reply_all()
comment_all('东北大学软件1403')

if __name__ == '__main__':
    fetch_statuses()
    #     print(s)
    # 取消关注一些账号, 用新买的号或者就是现在用的号
    # 每十分钟刷新一次timeline, 获取他的微博, 并获取私信或者回复消息
    # 调用机器人api, 发表评论, 回复消息
