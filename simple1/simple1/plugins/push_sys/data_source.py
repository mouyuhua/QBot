import requests

def pause_city(message: str):
    city_list = message.split(' ')
    return city_list

def daily_weather_information(city: str):
    key = '49596333b00a4c8f8880c76bef5d3fd8'
    area = city
    location_url = 'https://geoapi.qweather.com/v2/city/lookup?location='+str(area)+'&key='+key
    response = requests.get(url=location_url).json()
    area_code = response['code']

    if area_code == '200':
        area_id = response['location'][0]['id']
        area_name = response['location'][0]['name']
        area_adm = response['location'][0]['adm2']
        weather_result = get_weather(area_id, key)
        air_result = get_air(area_id, key)
        if area_adm == area_name:
            result = area_name+'今天的天气如下ヾ(•ω•`)o\n'+weather_result+'\n'+air_result
        else:
            result = area_adm+area_name+'今天的天气如下ヾ(•ω•`)o\n'+weather_result+'\n'+air_result
    else:
        result = -1

    return result

def get_weather(area_id, key):
    weather_url = 'https://devapi.qweather.com/v7/weather/3d?location='+area_id+'&key='+key
    response = requests.get(url=weather_url).json()
    if response['code'] == '200':
        temp_max = response['daily'][0]['tempMax']
        temp_min = response['daily'][0]['tempMin']
        weather_text_day = response['daily'][0]['textDay']
        weather_text_night = response['daily'][0]['textNight']
        # wind = response['daily']['windDir']
        result = '最高温度:'+temp_max+'℃\n最低温度：'+temp_min+'℃\n白天天气：'\
                 +weather_text_day+'\n夜间天气：'+weather_text_night
    else:
        result = '天气情况查询失败，请稍后再试(⊙x⊙;)'

    return result

def get_air(area_id, key):
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
