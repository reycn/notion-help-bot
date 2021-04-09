#!/usr/local/bin/python3.8
import logging
import re
from time import sleep
from configparser import ConfigParser
from sys import path as syspath
import time
from termcolor import cprint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from aiogram import types
# 初始化 bot
try:
    CHINESE_COUNT = 0
    cfg = ConfigParser()
    cfg.read(syspath[0] + '/config.ini')
    API_TOKEN = cfg.get('bot', 'token')
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
LAST_TIME = time.time() # 重复检测


# 定义函数


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
# 欢迎词
@dp.message_handler(commands=['start', 'welcome', 'about', 'help'])
async def start(message: types.Message):
    intro = '''进群先看置顶（更新时间：2020-10-10）

【社群简介】

本群为 Notion 爱好者自发组织的中文社群，主题以  Notion 为主，Notion 辅助效率工具、经验为辅。核心围绕提升个人生活品质、工作学习效率进行讨论。

⚠️注意：建议功能问题先询问客服，类似是否支持 xx 功能。在右下角的问号，Send us a message，你是 Notion 的用户，客服是权益的一部分，面对 Notion 客服可以使用中文。

* Notion 官方网站：https://www.notion.so
* Notion 中文频道：@NotionNews
* Notion 中文文档：http://t.cn/A627fCGz
* Notion 常见问题一览：https://linmi.cc/8663.html
* Notion 中文社区导航：http://t.cn/AiDsyH81
* 申请加入 Notion 中文社区：https://linmi.cc/n
* Notion 官方文档：http://t.cn/A627fCGz
* 学习使用快捷键：http://t.cn/A62OXLzE
* Notion 隐私协议：http://t.cn/A6L0VdyB
* 产品建议反馈：https://jinshuju.net/f/Fyvbfs

【群内规则】

* 禁止 NSFW
* 禁止人身攻击
* 禁止公开进行 Notion 账户购买和出售
* 禁止讨论政治敏感话题
* 禁止发布任何形式的广告，包括在名称中挂广告
* 禁止发布群组全体管理员认为不适于在此群组发布的消息'''
    await message.answer(intro)


####################################################################################################
# 命令
####################################################################################################
# 中英文
# @dp.message_handler(commands=['fy', 'tr'])
# async def fy_command(message: types.Message):
#     result = msg_trans(message, 3)  # None -> Chinese + English
#     await message.reply(result)


####################################################################################################
# 自然指令
####################################################################################################
@dp.message_handler(regexp='(汉化|中国版|本地化|本土化|在地化|中文|国内版|简体|繁体)')
    # '(Notion.*(有中文|没中文|汉化|中国版|本地化|本土化|在地化|中文))|((有中文|没中文|汉化|中国版|本地化|本土化|在地化|中文).*Notion)'
async def reply(message: types.Message):
    global LAST_TIME
    global CHINESE_COUNT
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    elif (time.time() - LAST_TIME) < 60:

        result = f'''再调戏我，打你屁屁，哼！  w(ﾟДﾟ)w.'''
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(0.5)
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
    else:
        result = f'''尚未发布，具体上线时间以官方消息为准。
这是提及中文的第 {CHINESE_COUNT} 次。


[FAQ](https://t.me/Notionso/31739)'''
        await bot.send_chat_action(message.chat.id, action="typing")
        CHINESE_COUNT += 1
        sleep(1.5)
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        with open(syspath[0] + '/logs/chinese.txt', 'w') as f:
            f.write(str(CHINESE_COUNT))
        LAST_TIME = time.time()


@dp.message_handler(regexp='(科学上网)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q：如何设置 Notion 的科学上网？
A：将以下域名加入工具规则——
loggly.com
segment.com
intercom.io
intercomcdn.com
amplitude.com
notion.so
amazonaws.com'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(加入社区|加社区)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q：如何加入 Notion 中文社区？
A：打开 https://linmi.cc/n ，在文章下方留言申请——
* 邮箱填写你的 Notion 注册邮箱。
* 网址无需填写。
* 每晚 9 点统一处理。
（注：申请表单为群主私人网站建立，邮箱填写对外隐藏，不会外泄，不会发送广告及其他内容。）'''
        await message.reply(result, reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(^|\b)hosts?($|\b)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q：如何找到对应的 Hosts
A：请看以下内容：
108.162.236.1/24 联通 走美国
172.64.32.1/24 移动 走香港
104.16.160.1/24 电信 走美国洛杉矶
172.64.0.0/24 电信 美国旧金山
104.20.157.0/24 联通 走日本
104.28.14.0/24 移动 走新加坡'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(有.*功能吗|功能.*吗|支持.*吗)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q：悬浮 TOC、脑图等功能支持有么？
A：无，建议功能问题先询问客服，类似是否支持 xx 功能。在右下角的问号，`Send us a message。`'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(表格)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: 表格功能支持吗？
A：无，但目前你可以通过公式生成： [表格生成器](https://www.notion.so/reycn/Notion-Table-Generator-c659abf41dfc4af7a69e5ae435b30d0c)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()

@dp.message_handler(regexp='(置顶)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''好嘞！ 这就是 [置顶](https://t.me/Notionso/123746)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()



@dp.message_handler(regexp='(侧边目录|浮动目录|悬浮目录|悬浮toc|悬浮 toc)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: 悬浮目录支持吗？
A：无，但目前你可以通过下列两种方式使用：
1、浏览器用户，安装以下插件之一 ——
－ [Notion Boost](https://gourav.io/notion-boost)、
－ [Notion X](https://github.com/scarsu/NotionX)；
2、客户端用户，安装 [Notion Enhancer](https://github.com/notion-enhancer/notion-enhancer)。'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(设置字体|改字体)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''只能选择字体风格（Sans、Serif、Mono），不能选择具体的字体'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(有模板|找模板)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: 在哪里能找到模板？
A：加入社区后：[模板中心](https://www.notion.so/cnotion/Notion-bc848f6560db42f6888c5104685d815d)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(有教程|找教程)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: 在哪里能找到教程？
A：加入社区后：[教程中心](https://www.notion.so/cnotion/Notion-054e065841894c4e8852afd629c9fbdc)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(访问慢|加载速度|访问速度|国内访问|速度慢)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: Notion 国内访问速度太慢，怎么加速？
    A：可以通过修改公益项目提供的加速 Hosts 后加速[Notion-Faster](https://www.notion.so/Notion-b39fd3de402e4841a7c2bd64625d1369)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()



@dp.message_handler(regexp='(访问慢|加载速度|访问速度|国内访问|速度慢)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: Notion 国内访问速度太慢，怎么加速？
    A：可以通过修改公益项目提供的加速 Hosts 后加速[Notion-Faster](https://www.notion.so/Notion-b39fd3de402e4841a7c2bd64625d1369)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()

@dp.message_handler(regexp='(clubhouse.*邀请码|邀请码.*clubhouse)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''一、这里是 Notion 社区，不是 Clubhouse 社区。
二、Linmi 个人站里提到的是 Clubhouse 的群，不是这个群。
三、「不要问『怎么获取邀请码』」。'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()

@dp.message_handler(regexp='(notion.*头像|头像.*notion)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: Notion 风格的头像如何获取？
A: 官方头像都是设计师专门绘制的，但你也可以[用一个项目生成类似的头像](https://www.openpeeps.com/)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()

@dp.message_handler(regexp='(notion.*博客|博客.*notion|Nobelium)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''Q: 怎么用 Notion 搭建博客？ 
A: 可以试试 [Nobelium](https://github.com/craigary/nobelium/blob/main/README-CN.md) 

它是一个使用 NextJS + Notion API 实现的，部署在 Vercel 上的静态博客系统。

> [效果预览](https://nobelium.vercel.app/)
> [项目开源地址](https://github.com/craigary/nobelium)
> [小白部署指南](https://blog.skylershu.com/post/nobelium-deployment-guide/)'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


@dp.message_handler(regexp='(机器人您好笨)')
async def reply(message: types.Message):
    global LAST_TIME
    clog(message)
    if (time.time() - LAST_TIME) < 10:
        print("Too frquent, ignored.")
        pass
    else:
        await bot.send_chat_action(message.chat.id, action="typing")
        sleep(1.5)
        result = '''啊哈 彼此彼此'''
        await message.reply(result, parse_mode="markdown", reply_markup=delete_btn)
        LAST_TIME = time.time()


####################################################################################################
# 私聊
####################################################################################################
# @dp.message_handler(
#     regexp=
#     '(Notion.*(有中文|没中文|汉化|中国版|本地化|本土化|在地化))|((有中文|没中文|汉化|中国版|本地化|本土化|在地化).*Notion)'
# )
# async def reply(message: types.Message):
#     chat_type = message.chat.type
#     if chat_type == 'private':
#         clog(message)

#         result = '没有中国版，详情请查阅：  [Notion 中文什么时候有？](https://linmi.cc/pin/18989)'
#         await message.reply(result, parse_mode="markdown")
#     else:  # 过滤所有群聊、频道
#         pass


@dp.message_handler(regexp='(科学上网)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = '''Q：如何设置 Notion 的科学上网？
    A：将以下域名加入工具规则——
    loggly.com
    segment.com
    intercom.io
    intercomcdn.com
    amplitude.com
    notion.so
    amazonaws.com'''
        await message.reply(result, parse_mode="markdown")
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler(regexp='(社区)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = '''Q：如何加入 Notion 中文社区？
A：打开 https://linmi.cc/n ，在文章下方留言申请——
* 邮箱填写你的 Notion 注册邮箱。
* 网址无需填写。
* 每晚 9 点统一处理。
（注：申请表单为群主私人网站建立，邮箱填写对外隐藏，不会外泄，不会发送广告及其他内容。）'''
        await message.reply(result)
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler(regexp='(^|\b)hosts?($|\b)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = '''Q：如何找到对应的 Hosts
A：请看以下内容：
108.162.236.1/24 联通 走美国
172.64.32.1/24 移动 走香港
104.16.160.1/24 电信 走美国洛杉矶
172.64.0.0/24 电信 美国旧金山
104.20.157.0/24 联通 走日本
104.28.14.0/24 移动 走新加坡'''
        await message.reply(result, parse_mode="markdown")
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler(regexp='(有.*功能吗|功能.*吗|支持.*吗)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = result = '''Q：悬浮 TOC、脑图等功能支持有么？
A：无，建议功能问题先询问客服，类似是否支持 xx 功能。在右下角的问号，`Send us a message。`'''
        await message.reply(result, parse_mode="markdown")
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler(regexp='(表格)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = '''Q: 表格功能支持吗？
A：无，但目前你可以通过公式生成： [表格生成器](https://www.notion.so/reycn/Notion-Table-Generator-c659abf41dfc4af7a69e5ae435b30d0c)'''
        await message.reply(result, parse_mode="markdown")
    else:  # 过滤所有群聊、频道
        pass


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


@dp.message_handler(regexp='(模板)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = '''Q: 在哪里能找到模板？
A：加入社区后：[模板中心](https://www.notion.so/cnotion/Notion-bc848f6560db42f6888c5104685d815d)'''
        await message.reply(result, parse_mode="markdown")
    else:  # 过滤所有群聊、频道
        pass


@dp.message_handler(regexp='(教程)')
async def reply(message: types.Message):
    chat_type = message.chat.type
    if chat_type == 'private':
        clog(message)
        result = '''Q: 在哪里能找到教程？
A：加入社区后：[教程中心](https://www.notion.so/cnotion/Notion-054e065841894c4e8852afd629c9fbdc)'''
        await message.reply(result, parse_mode="markdown")
    else:  # 过滤所有群聊、频道
        pass


if __name__ == '__main__':
    cprint('I\'m working now...', 'white', 'on_green')
    executor.start_polling(dp, skip_updates=True)
