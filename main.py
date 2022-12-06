#!/usr/local/bin/python3.8
import json
import logging
import re
import requests
import time
from configparser import ConfigParser
from sys import path as syspath
from time import sleep
from types import FunctionType

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQuery, InlineQueryResultArticle,
                           InputTextMessageContent)
# from revChatGPT.revChatGPT import Chatbot
from termcolor import cprint

from api import fetch_commands

# Initializing
try:
    CHINESE_COUNT = 0
    FREQ_THRESHOLD = 10
    cfg = ConfigParser()
    cfg.read(syspath[0] + '/config.ini')
    API_TOKEN = cfg.get('bot', 'token')
    AUTH = cfg.get('bot', 'auth')
    DB_ID = cfg.get('bot', 'db_id')
    COMMANDS = []
    COMMANDS = fetch_commands(auth=AUTH, db_id=DB_ID)
    with open(syspath[0] + '/logs/chinese.txt', 'r') as f:
        CHINESE_COUNT = int(f.read())

except Exception as e:
    cprint('Config file error, exit...', 'white', 'on_red')
    # capture_message('Config file error, exit...')
    print(e)
    exit()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
LAST_TIME = time.time()  # Duplicate detection


# Define functions
def clog(message):
    chat_type = message.chat.type
    user = message.from_user.username
    user_id = message.from_user.id
    group = message.chat.title
    chat_name = message.chat.username or message.from_user.username
    if group:
        cprint(
            f'[{chat_type}, %{group}, &{chat_name}, @{user}, #{user_id}] {message.text} ',
            'white', 'on_cyan')
    else:
        cprint(f'[{chat_type}, @{chat_name}, #{user_id}] {message.text} ',
               'white', 'on_cyan')


delete_btn = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
# delete_btn.insert(InlineKeyboardButton(text='👍', callback_data='vote'))
delete_btn.insert(InlineKeyboardButton(text='🗑️', callback_data='delete'))


####################################################################################################
# Welcome Message
@dp.message_handler(commands=['start', 'welcome', 'about', 'help'])
async def start(message: types.Message):
    intro = '''进群先看置顶（更新时间：2020-10-10）

【社群简介】

本群为 Notion 爱好者自发组织的中文社群，主题以  Notion 为主，Notion 辅助效率工具、经验为辅。核心围绕提升个人生活品质、工作学习效率进行讨论。

⚠️注意：建议功能问题先询问客服，类似是否支持 xx 功能。在右下角的问号，Send us a message，你是 Notion 的用户，客服是权益的一部分，面对 Notion 客服可以使用中文。


- Notion 官方网站 https://t.me/Notionso/199435
- Notion 中文社区： 
  ・ 导航 https://t.me/Notionso/199435
  ・ 申请加入 https://t.me/Notionso/199435
- Notion 中文社区电报群：@NotionSo
- Notion 中文社区电报频道：@NotionNews


🈲 入群请仔细阅读群规 https://t.me/Notionso/199435
🤔 更多资源及常见问题 https://t.me/Notionso/199435

❤️ 鼓励：提问前请多使用 Google 检索问题，若无答案，请在提问时说明需求与使用场景

⚠️ 注意：建议功能问题先询问客服，类似是否支持 xx 功能。如图，点击右下角右下角「❓」→ 「Send us a message」，你是 Notion 的用户，客服是权益的一部分，面对 Notion 客服可以使用中文。'''
    await message.answer(intro)


def replace_asking(prompt: str) -> str:
    result = prompt.replace('问问AI,', '').replace('问问AI，', '').replace(
        '问问ai，', '').replace('问问 ai，', '').replace('问问 AI', '')
    return result


@dp.message_handler(regexp='(问).*(AI)|(AI).*(问)')
async def ai_api(message: types.Message):
    # Get your config in JSON
    msg = await message.reply("好的，让我试试看……")
    await msg.edit_text(text="这个问题，机器也需要好好想想……")
    prompt = replace_asking(message.text)
    line_break = '''
'''
    print('正在处理 AI 提问: ' + prompt + '...')
    try:
        r = requests.get(f'http://127.0.0.1:8000/{prompt}')
        if r.status_code == 200:
            result = r.text.strip('\"')
            result = result.replace("\\n", line_break) + '© ChatGPT'
            await msg.edit_text(text="好像有答案了！")
            print('已收到 AI 反馈')
        else:
            result = '抱歉，我现在忙不过来，您等会儿再问问……'
        print(result)
        await bot.send_chat_action(message.chat.id, action="typing")
        await msg.edit_text(text=result, parse_mode="Markdown")
    except Exception as e:
        print(e)


####################################################################################################
# Group chats
####################################################################################################
# @dp.message_handler(regexp='(汉化|中国版|本地化|本土化|在地化|中文|国内版|简体|繁体)')
#     # '(Notion.*(有中文|没中文|汉化|中国版|本地化|本土化|在地化|中文))|((有中文|没中文|汉化|中国版|本地化|本土化|在地化|中文).*Notion)'
# async def reply(message: types.Message):
#     global LAST_TIME
#     global CHINESE_COUNT
#     clog(message)
#     if (time.time() - LAST_TIME) < 10:
#         print("Too frquent, ignored.")
#         pass
#     elif (time.time() - LAST_TIME) < 60:
#         result = f'''再调戏我，打你屁屁，哼！  w(ﾟДﾟ)w.'''
#         await bot.send_chat_action(message.chat.id, action="typing")
#         sleep(0.5)
#         await message.reply(result, parse_mode="Markdown", reply_markup=delete_btn)
#     else:
#         result = f'''这是提及中文的第 {CHINESE_COUNT} 次，官方中文正在灰度测试中，暂未正式发布。

# 中文相关问题请查看：[FAQ](https://t.me/Notionso/199403)'''
#         await bot.send_chat_action(message.chat.id, action="typing")
#         CHINESE_COUNT += 1
#         sleep(1.5)
#         await message.reply(result, parse_mode="Markdown", reply_markup=delete_btn)
#         with open(syspath[0] + '/logs/chinese.txt', 'w') as f:
#             f.write(str(CHINESE_COUNT))
#         LAST_TIME = time.time()

for command in COMMANDS:
    print(command[0])
    try:

        @dp.message_handler(regexp=command[0])
        async def group(message: types.Message, regexp):
            global LAST_TIME
            # chat_type = message.chat.type
            # if chat_type != 'private':
            clog(message)
            if (time.time() - LAST_TIME) < FREQ_THRESHOLD:
                print("Too frequent, ignored.")
                pass
            else:
                await bot.send_chat_action(message.chat.id, action="typing")
                pattern = regexp.re.pattern
                for i in COMMANDS:
                    if i[0] == pattern:
                        pattern_corr = i[1]
                        print(pattern_corr, pattern)
                # sleep(0.5)
                result = pattern_corr
                # print(result)
                await message.reply(result,
                                    parse_mode="Markdown",
                                    reply_markup=delete_btn)
                LAST_TIME = time.time()
    except Exception as e:
        cprint(f"Error ignored: {e}", 'white', 'on_yellow')
        pass

####################################################################################################
# Private Chat
####################################################################################################

# for command in COMMANDS:
#     # print(command[0], command[1])
#     @dp.message_handler(regexp=command[0])
#     async def private(message: types.Message):
#         chat_type = message.chat.type
#         if chat_type == 'private':
#             clog(message)
#             pattern = regexp.re.pattern
#             for i in COMMANDS:
#                 if i[0] == pattern:
#                     pattern_corr = i[1]
#                     print(pattern_corr, pattern)
#             result = pattern_corr
#             # print(command[0])
#             await message.reply(result, parse_mode="Markdown")
#         else:
#             pass

####################################################################################################
# Callback
####################################################################################################


@dp.message_handler(commands=['nn'])
async def ask_how_r_u(message: types.Message):
    await message.reply("Hi!\nHow are you?")


@dp.callback_query_handler(text='vote')
async def _(call: types.CallbackQuery):
    await call.answer(text="~~~")


@dp.callback_query_handler(text='delete')
async def _(call: types.CallbackQuery):
    global LAST_TIME
    await call.message.delete()
    LAST_TIME = LAST_TIME + 10
    await call.answer(text="该消息已为所有人删除")


if __name__ == '__main__':
    cprint('I\'m working now...', 'white', 'on_green')
    executor.start_polling(dp, skip_updates=True)
