# 谷歌翻译机器人(fanyi_bot)

![GitHub top language](https://img.shields.io/github/languages/top/reycn/fanyi_bot)
![version](https://img.shields.io/badge/version-2.1-green)  
为全世界语言提供中文翻译。  
[在 Telegram 上使用](https://t.me/fanyi_bot)

## 如何使用

- 私聊我，发送或转发需要翻译的文字，我会将其翻译为中文；
- 群聊中，添加我为管理员，用 "/fy" 命令回复需要翻译的消息
- [BETA] 任意聊天中 @fanyi_bot 调用翻译
- [BETA] 自动中译英。

## 最近更新

- 更换了更稳定的谷歌翻译 API
- 提供了中译英的新功能。
- 新增了任意调用功能

## 如何部署？

- 将你的 [Telegram Bot Token](https://core.telegram.org/bots#6-botfather) 放入 main.py 中的 16 行 TOKEN 处
- 安装依赖 `telepot`, `googletrans`, and `googletrans`
- 执行 `python3 main.py` / 或后台执行 `setsid python3 main.py`

## 代码依赖

- Python 3
- [telepot](https://github.com/nickoala/telepot) Python framework for Telegram Bot API
- [googletrans](https://github.com/ssut/py-googletrans) (unofficial) Googletrans: Free and Unlimited Google translate API for Python.
- [termcolor](https://github.com/hfeeki/termcolor) (fork version) fork of termcolor Python library
