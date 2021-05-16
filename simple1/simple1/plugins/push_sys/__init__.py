# --* v0.0.2 *--

from nonebot import plugin
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.drivers import Driver
from nonebot.adapters import Bot, Event
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from nonebot import get_driver
from .model import Push_information
from .data_source import daily_weather_information, pause_city
# from .config import Config

# global_config = get_driver().config
# config = Config(**global_config.dict())

push_list = []
start_time = []
bot_list = []

# @start.on_bot_connect()
# async def connect(bot: Bot):
#     if len(bot_list) != 0:
#         bot_list.pop()
#         bot_list.append(bot)
#     # await bot.send_msg(user_id=2902993382, mssage='connect')

push_schedule = AsyncIOScheduler()

push_start_event = plugin.on_command('开启天气预报', rule=to_me(), priority=19)
push_stop_event = plugin.on_command('关闭天气预报', rule=to_me(), priority=19)



@push_start_event.handle()
async def push_start(bot: Bot, event: Event, state: T_State):
    push_infor = Push_information()
    state['push_infor'] = push_infor
    des = event.get_event_description()
    des = des.split(' ')[3].split('@')
    args = str(event.get_message()).strip()
    # msg = str(event.get_message())

    if len(des) == 1:
        for i in push_list:
            if i.num == int(des[0]):
                await push_start_event.finish('start push already')
                break
        else:
            push_infor.type = 'friend'
            push_infor.num = int(des[0])
    else:
        des = des[1].split(':')[1].replace(']', '')
        for i in push_list:
            if i.num == int(des):
                await push_start_event.finish('start push already')
                break
        else:
            push_infor.type = 'group'
            push_infor.num = int(des)
    if args:
        state['citys'] = args

    if len(start_time) == 0:
        start_time.append('0')
        push_schedule.add_job(weather_push, 'cron', hour='7, 19', minute='30', jitter=120)
        push_schedule.start()

@push_start_event.got('citys', prompt='请设置要播报天气的城市')
async def city_set(bot: Bot, event: Event, state: T_State):
    citys = pause_city(state['citys'])
    push_infor = state['push_infor']
    push_infor.city = citys
    push_list.append(push_infor)
    bot_list.append(bot)
    await push_start_event.finish('start push')

@push_stop_event.handle()
async def push_stop(bot: Bot, event: Event):
    find_it = False
    des = event.get_event_description()
    des = des.split(' ')[3].split('@')
    if len(des) == 1:
        com = int(des[0])
    else:
        des = des[1].split(':')[1].replace(']', '')
        com = int(des)
    for i in push_list:
        if i.num == com:
            find_it = True
            break
    if find_it:
        push_list.remove(i)
        await push_stop_event.finish('stop push')
    else:
        await push_stop_event.finish("you haven't start push")


async def weather_push():
    bot = bot_list[0]
    for i in push_list:
        for city in i.city:
            information = daily_weather_information(city)
            if i.type == 'friend':
                await bot.send_msg(user_id=i.num, message=information)
            else:
                await bot.send_msg(group_id=i.num, message=information)
