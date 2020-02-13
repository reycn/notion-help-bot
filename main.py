#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-22 18:09:18
# @Author  : Reynard (rey@pku.edu.cn)
# @Link    : link
# @Version : 1.0.0

import time
import telepot
from sys import path as syspath
from configparser import ConfigParser
from termcolor import cprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from gtrans import trans

file = syspath[0] + '/config.ini'
cfg = ConfigParser()
cfg.read(file)
token = ''
try:
    cfg.get('bot', 'token')
    token = cfg.get('bot', 'token')
except Exception as e:
    print(e)
    print('Config file error, exit...')
    exit()

bot = telepot.Bot(token)
# bot.getMe()


def handle(msg):
    content_type, chat_type, chat_id, message_date, message_id = telepot.glance(
        msg, long=True)
    user_info = '用户' + str(chat_id) + content_type + chat_type + str(
        message_id)
    print(user_info)
    # print(str(msg))
    if content_type == 'text':

        if 'reply_to_message' in msg:
            msg_to_trans = msg['reply_to_message']
            command = get_text(msg)
            print(get_text(msg_to_trans), type(get_text(msg_to_trans)),
                  message_id)
        else:
            msg_to_trans = msg
            command = get_text(msg_to_trans)
        # if len(command) <= len('/fy@fanyi_bot'):
        #     pass
        # else:
        # print(get_text(msg_to_trans), type(get_text(msg_to_trans)), message_id)
        if chat_type == 'group' or chat_type == 'supergroup':
            if command == '/fy@fanyi_bot' or command == '/fy':
                pass
            elif command.startswith('/fy') or command.startswith(
                    '/fy@fanyi_bot'):
                result = trans(get_text(msg_to_trans).replace('/fy', ''))
                bot.sendMessage(
                    chat_id,
                    output(result),
                    #parse_mode='Markdown',
                    disable_web_page_preview=True)
            else:
                pass
        elif chat_type == 'private':
            help_msg = '开始使用：\n- 私聊我，发送或转发需要翻译的文字，我会将其翻译为中文；\n- 群聊中，添加我为管理员，用 `/fy` 命令回复需要翻译的消息\n- [BETA] 任意聊天中 @fanyi_bot 调用翻译\n- [BETA] 我也会将你发送的中文翻译为英文 😀。'
            if command.startswith('/start'):
                bot.sendMessage(chat_id, help_msg)
            elif command.startswith('/help'):
                bot.sendMessage(chat_id, help_msg)
            elif command.startswith('/fy'):
                result = trans(get_text(msg_to_trans).replace('/fy', ''))
                bot.sendMessage(
                    chat_id,
                    output(result),
                    #parse_mode='Markdown',
                    disable_web_page_preview=True)
            else:
                result = trans(get_text(msg_to_trans))
                bot.sendMessage(
                    chat_id,
                    output(result),
                    #parse_mode='Markdown',
                    disable_web_page_preview=True)


def output_clean(text):
    text = text.replace('（', '(').replace('）', ') ')
    text = text.replace('「', '“').replace('」', '”')
    text = text.replace('@', ' @')
    text = text.replace('：//', '://')
    text = text.replace('HTTPS：/ /', 'https://')
    #text = text.replace('//////////', '\n\n')
    text = text.replace('/////', '\n')
    text = text.replace('@fanyi_bot ', '')
    return text


def output(result, end_str_id=1):
    # end_str = '\n\n`─────`\n🤖 By [中文翻译机器人](https://t.me/fanyi_bot)'
    end_str = '\n─────\n🤖 By @fanyi_bot'
    if end_str_id == 2:
        end_str = '\n─────\n🤖 By @fanyi_bot'
    msg_str = output_clean(result)
    print(msg_str)
    msg_str += end_str
    return msg_str


def get_text(msg):
    if 'text' in msg:
        return msg['text']
    else:
        return msg['caption']


def inline_clean(text):
    text = text.replace('*', '\*')
    return (text)


def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg,
                                                     flavor='inline_query')
    print('Inline Query:', query_id, from_id, query_string)

    answers = [
        InlineQueryResultArticle(
            id='abc',
            title='翻译：' + query_string[:30] + '...',
            input_message_content=InputTextMessageContent(
                message_text=output(trans(query_string), 2),
                #parse_mode='Markdown',
                disable_web_page_preview=True))
    ]

    bot.answerInlineQuery(query_id, answers)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(
        msg, flavor='chosen_inline_result')
    print('选择:', result_id, from_id, query_string)


MessageLoop(
    bot, {
        'inline_query': on_inline_query,
        'chosen_inline_result': on_chosen_inline_result,
        'chat': handle
    }).run_as_thread()

cprint('Listening ...', 'green')

# Keep the program running.
while 1:
    time.sleep(10)
