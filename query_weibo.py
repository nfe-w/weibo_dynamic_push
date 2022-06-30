# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2021/4/23 16:32

import datetime
import json
import re
import time
from collections import deque

import util
from logger import logger
from push import push

DYNAMIC_DICT = {}
LEN_OF_DEQUE = 50


def query_dynamic(uid=None):
    if uid is None:
        return
    query_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=107603{uid}&count=25'.format(uid=uid)
    headers = get_headers(uid)
    response = util.requests_get(query_url, '查询动态状态', headers=headers, use_proxy=True)
    if util.check_response_is_ok(response):
        result = json.loads(str(response.content, 'utf-8'))
        cards = result['data']['cards']
        if len(cards) == 0:
            logger.info('【查询动态状态】【{uid}】动态列表为空'.format(uid=uid))
            return

        card = cards[0]

        # 跳过置顶
        if card['mblog'].get('isTop', None) == 1 or card['mblog'].get('mblogtype', None) == 2:
            # 如果只有置顶，则跳过
            if len(cards) == 1:
                return
            card = cards[1]
            # 新版微博支持两个置顶
            if card['mblog'].get('isTop', None) == 1 or card['mblog'].get('mblogtype', None) == 2:
                if len(cards) == 2:
                    return
                card = cards[2]

        mblog = card['mblog']
        mblog_id = mblog['id']
        user = mblog['user']
        screen_name = user['screen_name']

        if DYNAMIC_DICT.get(uid, None) is None:
            DYNAMIC_DICT[uid] = deque(maxlen=LEN_OF_DEQUE)
            for index in range(LEN_OF_DEQUE):
                if index < len(cards):
                    DYNAMIC_DICT[uid].appendleft(cards[index]['mblog']['id'])
            logger.info('【查询动态状态】【{screen_name}】动态初始化：{queue}'.format(screen_name=screen_name, queue=DYNAMIC_DICT[uid]))
            return

        if mblog_id not in DYNAMIC_DICT[uid]:
            previous_mblog_id = DYNAMIC_DICT[uid].pop()
            DYNAMIC_DICT[uid].append(previous_mblog_id)
            logger.info('【查询动态状态】【{}】上一条动态id[{}]，本条动态id[{}]'.format(screen_name, previous_mblog_id, mblog_id))
            DYNAMIC_DICT[uid].append(mblog_id)
            logger.info(DYNAMIC_DICT[uid])

            card_type = card['card_type']
            if card_type not in [9]:
                logger.info('【查询动态状态】【{screen_name}】动态有更新，但不在需要推送的动态类型列表中'.format(screen_name=screen_name))
                return

            # 如果动态发送日期早于昨天，则跳过（既能避免因api返回历史内容导致的误推送，也可以兼顾到前一天停止检测后产生的动态）
            created_at = time.strptime(mblog['created_at'], '%a %b %d %H:%M:%S %z %Y')
            created_at_ts = time.mktime(created_at)
            yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            yesterday_ts = time.mktime(time.strptime(yesterday, '%Y-%m-%d'))
            if created_at_ts < yesterday_ts:
                logger.info('【查询动态状态】【{screen_name}】动态有更新，但动态发送时间早于今天，可能是历史动态，不予推送'.format(screen_name=screen_name))
                return
            dynamic_time = time.strftime('%Y-%m-%d %H:%M:%S', created_at)

            content = None
            pic_url = None
            jump_url = None
            if card_type == 9:
                text = mblog['text']
                text = re.sub(r'<[^>]+>', '', text)
                content = mblog['raw_text'] if mblog.get('raw_text', None) is not None else text
                pic_url = mblog.get('original_pic', None)
                jump_url = card['scheme']
            logger.info('【查询动态状态】【{screen_name}】动态有更新，准备推送：{content}'.format(screen_name=screen_name, content=content[:30]))
            push.push_for_weibo_dynamic(screen_name, mblog_id, content, pic_url, jump_url, dynamic_time)


def get_headers(uid):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'mweibo-pwa': '1',
        'referer': 'https://m.weibo.cn/u/{}'.format(uid),
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'x-requested-with': 'XMLHttpRequest',
    }
