# -*- coding = utf-8 -*-
from nonebot import on_command
from nonebot import require
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests

weather_scheduler = require('nonebot_plugin_apscheduler').scheduler
weather_start = on_command("开启每日天气", rule=to_me(), priority=5)
weather_stop = on_command("关闭每日天气", rule=to_me(), priority=5)

#city = {}
push_group_list = []
push_friend_list = []
calltime = []

@weather_start.handle()
async def weather_start_puse(bot: Bot, event: Event, state: T_State):
    if len(calltime)==0:
        calltime.append('0')
        weather_scheduler.add_job(weather_puse, 'cron', minute='00, 15, 30, 45', args=[bot],misfire_grace_time=600)
    des = event.get_event_description()
    des = des.split(' ')[3].split('@')
    msg = str(event.get_message())
    if len(des) == 1:
        push_friend_list.append(int(des[0]))
    else:
        des = des[1].split(':')[1].replace(']', '')
        push_group_list.append(int(des))
    # await push_sys(city, bot)
    await weather_start.finish('start now')

@weather_stop.handle()
async def weather_stop_puse(bot: Bot, event: Event, state: T_State):
    des = event.get_event_description()
    des = des.split(' ')[3].split('@')
    if len(des) == 1:
        push_friend_list.remove(int(des[0]))
    else:
        des = des[1].split(':')[1].replace(']', '')
        push_group_list.remove(int(des))
    # await weather_puse_sys(False, '', bot)
    await weather_stop.finish('stop now')

# async def push_sys(city, bot):
#     if start_with:
#         start_with = False


async def weather_puse(bot: Bot):
    city = 'xingtai'
    for i in push_group_list:
        city_weather = await get_weather(city)
        await bot.send_group_msg(group_id=i,message=city_weather)
    for i in push_friend_list:
        city_weather = await get_weather(city)
        await bot.send_msg(user_id=i, message=city_weather)

async def get_weather(city: str):
    key = '49596333b00a4c8f8880c76bef5d3fd8'
    area = city
    location_url = 'https://geoapi.qweather.com/v2/city/lookup?location='+str(area)+'&key='+key
    response = requests.get(url=location_url).json()
    area_code = response['code']

    if area_code == '200':
        area_id = response['location'][0]['id']
        area_name = response['location'][0]['name']
        area_adm = response['location'][0]['adm2']
        weather_result = weather_now(area_id, area_name, key)
        air_result = get_air(area_id, area_name, key)
        if area_adm == area_name:
            result = area_name+'今天的天气如下ヾ(•ω•`)o\n'+weather_result+'\n'+air_result
        else:
            result = area_adm+area_name+'今天的天气如下ヾ(•ω•`)o\n'+weather_result+'\n'+air_result
    else:
        result = -1

    return result

def weather_now(area_id, area_name, key):
    weather_url = 'https://devapi.qweather.com/v7/weather/3d?location='+area_id+'&key='+key
    response = requests.get(url=weather_url).json()
    if response['code'] == '200':
        temp_max = response['daily'][0]['tempMax']
        temp_min = response['daily'][0]['tempMin']
        weather_text_day = response['daily'][0]['textDay']
        weather_text_night = response['daily'][0]['textNight']
        # wind = response['daily']['windDir']
        result = '最高温度:'+temp_max+'\n最低温度：'+temp_min+'\n白天天气：'\
                 +weather_text_day+'\n夜间天气：'+weather_text_night
    else:
        result = '天气情况查询失败，请稍后再试(⊙x⊙;)'

    return result

def get_air(area_id, area_name, key):
    air_url = 'https://devapi.qweather.com/v7/air/now?location='+area_id+'&key='+key
    response = requests.get(url=air_url).json()
    if response['code'] == '200':
        pm2_5 = response['now']['pm2p5']
        category = response['now']['category']
        aqi = response['now']['aqi']
        result = '空气质量指数：'+aqi+'  '+category+'\nPM2.5:'+pm2_5
    else:
        result = '空气情况查询失败了o((>ω< ))o'
    return result
