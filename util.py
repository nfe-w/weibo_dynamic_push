# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2021/3/28 01:00

import random

import requests

from logger import logger
from proxy import my_proxy

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
]


def get_random_useragent():
    return random.choice(USER_AGENTS)


def requests_get(url, module_name='未指定', headers=None, params=None, use_proxy=False):
    if headers is None:
        headers = {}
    headers = dict({
        'User-Agent': get_random_useragent()
    }, **headers)
    proxies = _get_proxy() if use_proxy else None
    try:
        response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=10)
    except Exception as e:
        logger.error("【{}】：{}".format(module_name, e))
        return None
    return response


def requests_post(url, module_name='未指定', headers=None, params=None, data=None, json=None, use_proxy=False):
    if headers is None:
        headers = {}
    headers = dict({
        'User-Agent': get_random_useragent()
    }, **headers)
    proxies = _get_proxy() if use_proxy else None
    try:
        response = requests.post(url, headers=headers, params=params, data=data, json=json, proxies=proxies, timeout=10)
    except Exception as e:
        logger.error("【{}】：{}".format(module_name, e))
        return None
    return response


def _get_proxy():
    if my_proxy.enable == 'true':
        proxy_ip = my_proxy.current_proxy_ip
        if proxy_ip is None:
            return None
        else:
            return {
                "http": "http://{}".format(proxy_ip)
            }


def check_response_is_ok(response=None):
    if response is None:
        return False
    if response.status_code != requests.codes.OK:
        logger.error('status: {}, url: {}'.format(response.status_code, response.url))
        return False
    return True
