#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-22 18:41:57
# @Author  : Reynard (rey@pku.edu.cn)
# @Link    : link
# @Version : 1.0.0

import re
from googletrans import Translator
from termcolor import cprint


def text_clean(text):
    # TODO: 文本清洗
    text = re.sub('(\[转发自.*\])\n', '', text)
    text = text.replace('\n', '/////')
    text = text.replace('#', ' ')
    text = filter_emoji(text)
    return (text)


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        res = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        res = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return res.sub(restr, desstr)


def big5(text):
    try:
        text.encode('big5hkscs')
        cprint('繁体', 'white', 'on_grey')
        result = True
    except Exception as e:
        cprint('简体' + e, 'white', 'on_grey')
        result = False
    return result


def trans(text, lang='zh-CN', detect=1):
    text = text_clean(text)
    tr = Translator()
    if lang == 'en':
        result = '🇺🇸 ' + tr.translate(text, dest='en').text
    elif lang == 'zh':
        result = '🇨🇳 ' + tr.translate(text, dest='zh-CN').text
    else:
        if tr.detect(text).lang == 'zh-CN':
            result = '🇨🇳 ' + tr.translate(text, dest='zh-CN').text + '\n\n🇺🇸 ' \
                + tr.translate(text, dest='en').text
            # print(result)
        else:
            result = '🇨🇳 ' + tr.translate(text, dest='zh-CN').text + '\n\n🇺🇸 ' \
                + text
    return result


if __name__ == "__main__":
    pass
