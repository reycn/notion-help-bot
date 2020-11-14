#!/usr/bin/python3.7
import logging
import re
from clean import output
from configparser import ConfigParser
from gtrans import trans
from stathat import StatHat
from sys import path as syspath
from termcolor import cprint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from sentry_sdk import init, capture_message


# 初始化 bot
try:
    cfg = ConfigParser()
    cfg.read(syspath[0] + '/config.ini')
    API_TOKEN = cfg.get('bot', 'token')
    STAT = cfg.get('stat', 'enabled')  # 不启用则不使用统计
    STAT_ACCOUNT = cfg.get('stat', 'account')
    STAT_INSTANCE = cfg.get('stat', 'instance')
    SENTRY_SDK = cfg.get('sentry', 'sdk')
    # LANG = cfg.get('lang', 'destination') # 暂时没有使用

    
except Exception as e:
    cprint('Config file error, exit...', 'white', 'on_red')
    capture_message('Config file error, exit...')
    print(e)
    exit()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
init( SENTRY_SDK, traces_sample_rate=1.0)

# 定义函数
def trans_c(text, lang='zh-CN', detect=1):
    translated_cleaned = output(trans(text, lang))
    if STAT:
        try:
            stathat = StatHat()
            stathat.ez_post_count(STAT_ACCOUNT, STAT_INSTANCE, 1)
        except Exception as e:
            cprint('Request susceed but stat failed!' + e, 'white', 'on_red')
            capture_message('Request susceed but stat failed!')
    return translated_cleaned


def msg_trans(message: types.Message,
              offset: int = 0,
              lang: str = None,
              reg: str = None):
    if message.reply_to_message:  # 如果是回复则取所回复消息文本
        text = message.reply_to_message.text
    else:  # 如果不是回复则取命令后文本
        text = message.text[offset:]  # 去除命令文本
    text = text.replace('@fanyi_bot', '').strip()
    if reg:
        text = re.sub(reg, '', text)

    if len(text) == 0 :
        if message.reply_to_message:
            clog(message)
            # capture_message(message)
            result = trans_c(text, lang)
            return (result)
        else:
            pass
    else:
        clog(message)
        # capture_message(message)
        result = trans_c(text, lang)
        return (result)


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
        # capture_message(f'[{chat_type}, %{group}, &{chat_name}, @{user}, #{user_id}] {message.text} ')
    else:
        cprint(f'[{chat_type}, @{chat_name}, #{user_id}] {message.text} ',
               'white', 'on_cyan')
        # capture_message(f'[{chat_type}, @{chat_name}, #{user_id}] {message.text} ')


####################################################################################################
# 欢迎词
@dp.message_handler(commands=['start', 'welcome', 'about', 'help'])
async def start(message: types.Message):
    intro = '''使用说明：
- 私聊机器人，自动翻译文字消息；
- 群聊中添加机器人，使用命令翻译指定消息；
- 任意聊天框，输入 @fanyi_bot 实时翻译。

使用样例：
/fy 检测语言并翻译
/zh Translate a sentence into Chinese.
/en 翻译到英文

最近更新
- [2020.11.14] 修复了一个上游引起的 BUG

加入群组 @fanyi_group 参与讨论。'''
    await message.answer(intro)


####################################################################################################
# 翻译命令
####################################################################################################
# 中英文
@dp.message_handler(commands=['fy', 'tr', '翻译'])
async def fy_command(message: types.Message):
    result = msg_trans(message, 3)  # None -> Chinese + English
    await message.reply(result)


# 中文
@dp.message_handler(commands=['zh'])
async def zh(message: types.Message):
    result = msg_trans(message, 3, 'zh')
    await message.reply(result)


# 英文
@dp.message_handler(commands=['en'])
async def en(message: types.Message):
    result = msg_trans(message, 3, 'en')
    await message.reply(result)


####################################################################################################
# 自然指令
####################################################################################################
@dp.message_handler(regexp='^(translate|trans|tran|翻译) ')
async def fy_keyword_zh(message: types.Message):
    result = msg_trans(message, reg='^(translate|trans|tran|翻译) ')
    await message.reply(result)


@dp.message_handler(regexp='^(英文|英语|English|en) ')
async def en_keyword_zh(message: types.Message):
    result = msg_trans(message, lang='en', reg='^(英文|英语|English|en) ')
    await message.reply(result)


@dp.message_handler(regexp='^(中文|Chinese|zh) ')
async def zh_keyword(message: types.Message):
    result = msg_trans(message, lang='zh', reg='^(中文|Chinese|zh) ')
    await message.reply(result)

@dp.message_handler(regexp='^(translate|trans|tran|翻译)')
async def fy_keyword_zh(message: types.Message):
    if message.reply_to_message:
        result = msg_trans(message, reg='^(translate|trans|tran|翻译)')
        await message.reply(result)


@dp.message_handler(regexp='^(英文|English|en)')
async def en_keyword_zh(message: types.Message):
    if message.reply_to_message:
        result = msg_trans(message, lang='en', reg='^(英文|English|en)')
        await message.reply(result)


@dp.message_handler(regexp='^(中文|Chinese|zh)')
async def zh_keyword(message: types.Message):
    if message.reply_to_message:
        result = msg_trans(message, lang='zh', reg='^(中文|Chinese|zh)')
        await message.reply(result)
####################################################################################################
# 私聊自动检测语言并翻译
####################################################################################################
@dp.message_handler(content_types=types.message.ContentType.TEXT)
async def text_message(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        # capture_message(message)
        result = trans_c(message.text)
        await message.reply(result)
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler()
async def other_types(message: types.Message):
    print('Other types')
    # capture_message('Other types')
    try:
        clog(message)
        # capture_message(message)
        result = trans_c(message.text)
    except Exception as e:
        print('Exception', e)
        capture_message('Exception', e)
        result = '? ? ?'
    await message.answer(result)


# 行内查询
@dp.inline_handler()
async def inline(inline_query: InlineQuery):
    text = inline_query.query or '翻译…'
    user = inline_query.from_user.username
    user_id = inline_query.from_user.id
    if len(text) >= 256:
        end_str = '\n\n(达到长度限制，请私聊翻译全文）'
    else:
        end_str = ''
    if text == '翻译…':
        pass
    else:
        cprint(f'[inline, @{user}, #{user_id}] {text} ', 'white', 'on_cyan')
        # capture_message(f'[inline, @{user}, #{user_id}] {text} ')
        zh_str = trans_c(text, 'zh').replace(end_str, '')
        en_str = trans_c(text, 'en').replace(end_str, '')
        items = [
            InlineQueryResultArticle(
                id=0,
                title=f'自动检测 / Auto detection',
                description=f'{zh_str[:40]}... {en_str[:40]}...'.strip(),
                thumb_width=0,
                input_message_content=InputTextMessageContent(
                    f'{zh_str}\n{en_str}{end_str}',
                    disable_web_page_preview=True),
            ),
            InlineQueryResultArticle(
                id=1,
                title='英文 / English',
                description=f'{en_str}'.strip(),
                thumb_width=0,
                input_message_content=InputTextMessageContent(
                    f'{en_str}{end_str}', disable_web_page_preview=True),
            ),
            InlineQueryResultArticle(
                id=2,
                title='中文 / Simplified Chinese',
                description=f'{zh_str}'.strip(),
                thumb_width=0,
                input_message_content=InputTextMessageContent(
                    f'{zh_str}{end_str}', disable_web_page_preview=True),
            )
        ]
        await bot.answer_inline_query(inline_query.id,
                                      results=items,
                                      cache_time=300)


if __name__ == '__main__':
    cprint('I\'m working now...', 'white', 'on_green')
    capture_message('I\'m working now...')
    executor.start_polling(dp, skip_updates=True)
