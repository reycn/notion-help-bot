#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-22 18:41:57
# @Author  : Reynard (oyrx@vip.qq.com)
# @Link    : link
# @Version : 1.0.0

# 引入用到的模块
# import urllib
import requests
import json
import re
from googletrans import Translator
from termcolor import cprint


def text_clean(text):
    # TODO: 文本清洗
    text = re.sub('(\[转发自.*\])\n', '', text)
    #text = re.sub("(#.*)", '', text)
    text = text.replace('\n', '/////')
    text = text.replace('#', ' ')
    # text = urllib.quote(text)
    print(text)
    return (text)


def big5(text):
    try:
        text.encode('big5hkscs')
        print('繁体')
        result = True
    except Exception as e:
        print('简体', e)
        result = False
    return result


def trans(text, lang='zh-CN', detect=1):
    text = text_clean(text)
    tr = Translator()
    #cprint(tr.detect(text), 'red')
    if tr.detect(text).lang == 'zh-CN':
        result = tr.translate(text, dest='zh-CN').text + '\n\n' \
               + tr.translate(text, dest='en').text
        print(result)
    else:
        result = tr.translate(text, dest='zh-CN').text + '\n\n' \
               + text
    return result


if __name__ == "__main__":
    result = trans(
        "[转发自用户 Reynard]\n[转发自用户 IFTTT]\nYou have successfully connected the channel @apex_info. You can now use it with Telegram Applets on IFTTT (https://ifttt.com/telegram) (https://ifttt.com/telegram)."
    )
    print(result[0].replace('.', '。') + '\n\n(源语言被自动识别为: ' +
          result[1].upper() +
          ', 由 Google Translate(https://translate.google.com) 提供。)')
    pass
