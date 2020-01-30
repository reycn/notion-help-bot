#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-22 18:09:18
# @Author  : Reynard (rey@pku.edu.cn)
# @Link    : link
# @Version : 1.0.0

# import telepot
# from telepot.loop import MessageLoop
# import sys
import asyncio
import telepot
from gtrans import trans as trans
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
# from pprint import pprint
# bot = telepot.Bot('604475928:AAE2a20ewitpPtkn4fI4WkwHFoJnHZ0xyf8')


class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    async def on_chat_message(self, msg):
        self._count += 1
        print(trans('Text'))
        await self.sender.sendMessage(self._count)


TOKEN = '604475928:AAE2a20ewitpPtkn4fI4WkwHFoJnHZ0xyf8'  # get token from command-line

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
