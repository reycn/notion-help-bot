# 谷歌翻译机器人(fanyi_bot)

![GitHub top language](https://img.shields.io/github/languages/top/reycn/fanyi_bot)
[![codebeat badge](https://codebeat.co/badges/660fd5c4-7218-4408-b57a-94877e55ffdb)](https://codebeat.co/projects/github-com-reycn-fanyi_bot-master) ![version](https://img.shields.io/badge/version-2.4-red) ![License](https://img.shields.io/badge/license-MIT-000000.svg) [![Served](https://img.shields.io/badge/dynamic/json?color=27ae60&label=served&query=%24%5B0%5D.points%5B0%5D.value&suffix=%20times&url=https%3A%2F%2Fwww.stathat.com%2Fx%2FTBKGENBCfgrMmHY4GCpo%2Fdata%2FYTlb%3Fsummary%3D10y10y)](https://www.stathat.com/s/9xOlCBfnl1kj)  
为全世界语言提供中文翻译。  
[在 Telegram 上使用](https://t.me/fanyi_bot)

## 如何使用?

- 私聊机器人，自动翻译文字消息；
- 群聊中添加机器人，使用命令翻译指定消息；
- 任意聊天框，输入 @fanyi_bot 实时翻译。


## 最近更新
- [2020.12.05] 彻底解决 API 问题
- [2020.11.14] 脏解决 API 问题
- [2020.08.11] 修复交互细节
- [2020.08.05] 机器人现已无需管理员权限
- [2020.08.04] 使用最新模型，提升翻译质量

## 如何部署到自己的服务器？

- 按照 `confi.template` 文件的格式新建 `config.ini` 配置文件，将你的 [Telegram Bot Token](https://core.telegram.org/bots#6-botfather) 放入该文件中
- `pip install -r requirements.txt` 安装依赖 `aiogram`, `termcolor`, and `googletrans`
- 执行 `python3 main.py` / 或后台执行 `setsid python3 main.py`

## 功能预览

- 私聊或有管理员权限的群聊中直接翻译

  <img src="https://github.com/reycn/fanyi_bot/blob/master/res/chat.jpg?raw=true" width="300"></img>

- 在任意聊天窗口 @fanyi_bot 通过 inline query 直接查询

  <img src="https://github.com/reycn/fanyi_bot/blob/master/res/inline.jpg?raw=true" width="300"></img>

## 代码依赖

- Python >= 3.7
- [aiogram](https://github.com/aiogram/aiogram) Is a pretty simple and fully asynchronous framework for Telegram Bot API written in Python 3.7 with asyncio and aiohttp.
- [googletrans](https://github.com/ssut/py-googletrans) (unofficial) Googletrans: Free and Unlimited Google translate API for Python.
- [termcolor](https://github.com/hfeeki/termcolor) (fork version) fork of termcolor Python library
