# -*- coding = utf-8 -*-
from nonebot import plugin
from nonebot.adapters import Bot, Event

request_event = plugin.on_request(priority=20)

@request_event.handle()
async def deal_request_event(bot: Bot, event: Event):
    event_name = event.get_event_name()
    if event_name == 'request.friend':
        imfor = event.get_event_description().split("'")
        flag = imfor[-2].replace("'", "")
        await bot.set_friend_add_request(flag=flag, approve=False)
    elif event_name == 'request.group.invite':
        imfor = event.get_event_description().split("'")
        flag = imfor[-2].replace("'", "")
        sub_type = imfor[15].replace("'","")
        await bot.set_group_add_request(flag=flag, sub_type=sub_type, approve=True)
    elif event_name == 'request.group.add':
        imfor = event.get_event_description().split("'")
        flag = imfor[-2].replace("'", "")
        sub_type = imfor[15].replace("'","")
        await bot.set_group_add_request(flag=flag, sub_type=sub_type, approve=True)
    await request_event.finish()
