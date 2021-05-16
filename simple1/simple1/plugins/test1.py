# -*- coding = utf-8 -*-
import time
from nonebot import plugin
from nonebot import require
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

# scheduler = require('nonebot_plugin_apscheduler').scheduler
# test_event = plugin.on_notice(priority=3,block=False)
#
# @test_event.handle()
# async def event_deal(bot: Bot, event: Event, state: T_State):
#     message_event = event.get_log_string()
#     message_event_name = event.get_event_name()
#     message_event_des = event.get_event_description()
#     # group_list = await bot.get_group_list()
#     # friends_list = await bot.get_friend_list()
#     # #list = [{'i':20020, 'j':10000}]
#     # for i in group_list:
#     #     await test_event.send(str(i['group_id']))
#     # for i in friends_list:
#     #     await test_event.send(str(i['user_id'])+i['nickname'])
#     await test_event.send(message_event)
#     await test_event.send(message_event_name)
#     await test_event.send(message_event_des)
#     await test_event.finish()
#
# test_event_re = plugin.on_request(priority=3,block=False)
#
# @test_event_re.handle()
# async def re_event_deal(bot: Bot, event: Event, state: T_State):
#     message_event_name = event.get_event_name()
#     message_event_des = event.get_event_description()
#     # event_type = event.get
#     await test_event_re.send(message_event_name)
#     await test_event_re.send(message_event_des)
#     # await test_event.send(event_type)
#     await test_event_re.finish()


#

# @test_event_msg.handle()
# async def msg_event_deal(bot: Bot, event: Event, state: T_State):
#     message_event_name = event.get_event_name()
#     message_event_des = event.get_event_description()
#     message = str(event.get_message())
#     await test_event_msg.send(message_event_name)
#     await test_event_msg.send(message_event_des)
#     await test_event_msg.send(message)
#
#     # scheduler.add_job(send_time, 'cron', second='*/1', args=[message_event_id])
#     #scheduler.pause()
#
#     await test_event_msg.finish('finish')

# async def send_time(state):
#     q_id = state
#     await Bot.call_api(api='send_msg', message='hello'+str(q_id)+'\ntime is'+str(time.ctime()))
#     #time.sleep(5)

test_event_com = plugin.on_command('r',rule=to_me(), priority=3,block=False)
async def msg_event_deal(bot: Bot, event: Event, state: T_State):
    message_event_name = event.get_event_name()
    message_event_des = event.get_event_description()
    message = event.get_plaintext()
    await test_event_com.send(message_event_name)
    await test_event_com.send(message_event_des)
    await test_event_com.send(message)
    await test_event_com.finish('finish')
