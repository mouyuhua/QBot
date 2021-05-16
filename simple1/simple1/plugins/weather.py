# -*- coding = utf-8 -*-
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests

weather = on_command("天气", rule=to_me(), priority=6)

@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值
        city_weather = await get_weather(state["city"])
        if city_weather == -1:
            await weather.finish("查询城市有误请重新查询")
        await weather.finish(city_weather)

@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    city = state["city"]
    city_weather = await get_weather(city)
    if city_weather == -1:
        await weather.reject("你想查询的城市暂不支持，请重新输入！")
    await weather.finish(city_weather)

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
            result = area_name+'查询结果如下ヾ(•ω•`)o\n'+weather_result+'\n'+air_result
        else:
            result = area_adm+area_name+'查询结果如下ヾ(•ω•`)o\n'+weather_result+'\n'+air_result
    else:
        result = -1

    return result

def weather_now(area_id, area_name, key):
    weather_url = 'https://devapi.qweather.com/v7/weather/now?location='+area_id+'&key='+key
    response = requests.get(url=weather_url).json()
    if response['code'] == '200':
        temp = response['now']['temp']+'℃'
        feels_like = response['now']['feelsLike']+'℃'
        weather_text = response['now']['text']
        wind = response['now']['windDir']
        result = '天气:'+weather_text+'\n温度：'+temp+'\n体感温度：'+feels_like+'\n风向：'+wind
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
