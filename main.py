import logging
from sys import path as syspath
from configparser import ConfigParser
from gtrans import trans
from termcolor import cprint
from clean import output
from stathat import StatHat
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

# 初始化 bot
try:
    cfg = ConfigParser()
    cfg.read(syspath[0] + '/config.ini')
    API_TOKEN = cfg.get('bot', 'token')
    STAT = cfg.get('stat', 'enabled')  # 不启用则不使用统计
    STAT_ACCOUNT = cfg.get('stat', 'account')
    STAT_INSTANCE = cfg.get('stat', 'instance')
    # LANG = cfg.get('lang', 'destination') # 暂时没有使用
except Exception as e:
    cprint('Config file error, exit...', 'white', 'on_red')
    print(e)
    exit()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# 定义函数
def trans_c(text, lang='zh-CN', detect=1):
    translated_cleaned = output(trans(text, lang))
    if STAT:
        try:
            stathat = StatHat()
            stathat.ez_post_count(STAT_ACCOUNT, STAT_INSTANCE, 1)
        except Exception as e:
            cprint('Request susceed but stat failed!' + e, 'white', 'on_red')
    return translated_cleaned


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


####################################################################################################
# 定义处理
# 欢迎词
@dp.message_handler(commands=['start', 'welcome', 'about', 'help'])
async def start(message: types.Message):
    intro = '''为全世界语言提供中文翻译。\n
如何使用？
- 私聊我，发送或转发需要翻译的文字；
- 群聊授予消息读取权限，用 "/fy" 后接文字或回复需翻译的文本；
- 在私聊或群聊中，使用 "/en" 或 "/zh" 指定翻译语言；
- 任意聊天中 @fanyi_bot 调用行内请求(inline query) 选择目标语言进行翻译。
\n
最近更新了什么？
- [BETA] 更换了异步框架
- [BETA] 提供了行内请求 (inline query) 实时转译
- [BETA] 提供了指定翻译语言的功能

群聊为何需要管理员权限？
- Telegram 中，不是管理员的机器人无法读取群消息，也就无法翻译。\n
服务掉线请联系 @reycn，反馈请到 @fanyi_group。'''
    await message.answer(intro)


# 禁止翻译套娃
@dp.message_handler(regexp='(🤖 By @fanyi_bot)')
async def rerere(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        await message.reply('🌚 禁止套娃！')
    else:
        pass


# # 测试命令
# @dp.message_handler(commands=['tp'])
# async def tp(message: types.Message):
#     chat_type = message.chat.type
#     cprint(chat_type, 'white', 'on_yellow')
#     await message.reply(chat_type)


# 翻译命令
@dp.message_handler(commands=['fy', 'tr'])
async def fy(message: types.Message):
    if message.reply_to_message:  # 如果是回复则取所回复消息文本
        text = message.reply_to_message.text
    else:  # 如果不是回复则取命令后文本
        text = message.text[3:]
    text = text.replace('@fanyi_bot', '').replace('@fanyi_bot', '').strip()
    if len(text) == 0:
        pass
    else:
        clog(message)
        result = trans_c(text)
        await message.reply(result)


# 指定翻译为英文
@dp.message_handler(commands=['en'])
async def en(message: types.Message):
    if message.reply_to_message:  # 如果是回复则取所回复消息文本
        text = message.reply_to_message.text
    else:  # 如果不是回复则取命令后文本
        text = message.text[3:]
    text = text.replace('@fanyi_bot', '').replace('@fanyi_bot', '').strip()
    if len(text) == 0:
        pass
    else:
        clog(message)
        result = trans_c(text, 'en')
        await message.reply(result)


# 指定翻译为中文
@dp.message_handler(commands=['zh'])
async def zh(message: types.Message):
    if message.reply_to_message:  # 如果是回复则取所回复消息文本
        text = message.reply_to_message.text
    else:  # 如果不是回复则取命令后文本
        text = message.text[3:]
    text = text.replace('@fanyi_bot', '').replace('@fanyi_bot', '').strip()
    if len(text) == 0:
        pass
    else:
        clog(message)
        result = trans_c(text, 'zh')
        await message.reply(result)


# 私聊自动检测语言并翻译
@dp.message_handler(content_types=types.message.ContentType.TEXT)
async def text_message(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = trans_c(message.text).replace('\n\n🤖 By @fanyi_bot', '')
        await message.reply(result)
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler()
async def other_types(message: types.Message):
    print('Other types')
    try:
        clog(message)
        result = trans_c(message.text)
    except Exception as e:
        print('Exception', e)
        result = '🌚 ? ? ?'
    await message.answer(result)


# 行内查询
@dp.inline_handler()
async def inline(inline_query: InlineQuery):
    text = inline_query.query or '翻译…'
    user = inline_query.from_user.username
    user_id = inline_query.from_user.id
    if len(text) >= 256:
        end_str = '\n\n(达到行内查询长度限制，请私聊 bot 翻译全文）\n🤖 By @fanyi_bot'
    else:
        end_str = '\n\n🤖 By @fanyi_bot'
    if text == '翻译…':
        pass
    else:
        cprint(f'[inline, @{user}, #{user_id}] {text} ', 'white', 'on_cyan')
        zh_str = trans_c(text, 'zh').replace(end_str, '')
        en_str = trans_c(text, 'en').replace(end_str, '')
        items = [
            InlineQueryResultArticle(
                id=0,
                title=f'检测并翻译到中英文 / Auto detection',
                description=f'{zh_str[2:40]}... {en_str[2:40]}...'.replace(
                    '🇨🇳', '').replace('🇺🇸', '').strip(),
                thumb_width=0,
                input_message_content=InputTextMessageContent(
                    f'{zh_str}\n\n{en_str}{end_str}',
                    disable_web_page_preview=True),
            ),
            InlineQueryResultArticle(
                id=1,
                title='英文 / English',
                description=f'{en_str}'.replace('🇨🇳', '').replace('🇺🇸',
                                                                  '').strip(),
                thumb_width=0,
                input_message_content=InputTextMessageContent(
                    f'{en_str}{end_str}', disable_web_page_preview=True),
            ),
            InlineQueryResultArticle(
                id=2,
                title='中文 / Simplefiled Chinese',
                description=f'{zh_str}'.replace('🇨🇳', '').replace('🇺🇸',
                                                                  '').strip(),
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
    executor.start_polling(dp, skip_updates=True)