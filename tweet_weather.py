#!/usr/bin/env python
# coding: utf-8

import sys
import os
import xml_parser
import datetime
from twython import Twython

def predict_weather(url, area, str_date, name_date):
    date = xml_parser.set_weather_info(url, area, str_date);

    weather_name =  xml_parser.get_weather_name(date)
    list_weather_rain = xml_parser.get_rain_fall_chance(date)
    # print list_rain_fall_chance.items()

    message_intro = name_date + 'の' + area + 'の天気は' + weather_name + 'です。\n'

    if '雨' in weather_name or 'くもり' in weather_name :
        i = 0
        rain_chance = 0
        message_rain = '降水確率は、\n'

        for weather_rain in list_weather_rain :
            # print 'HOUR:' + hour + ', CHANCE:' + chance
            if rain_chance < weather_rain :
                rain_chance = weather_rain
            message_rain += str(i*6) + '時から' + str((i+1)*6) + '時が' + str(weather_rain) + '%\n'
            i += 1

        message_weather = message_rain + 'となっています。'
        if int(rain_chance) > 30 :
            message_weather += '雨にお気をつけて！'
        else :
            message_weather += 'どんより天気ですが頑張っていきましょう！'
    else :
        if '今日' in str_date:
            message_weather = '天気が良いので今日も頑張っていきましょう！'
        else :
            message_weather = '天気が良いので明日も頑張っていきましょう！'

    if '明日' in str_date :
        message_weather += 'おやすみなさい。'

    return message_intro + message_weather


if __name__ == '__main__':
    param = sys.argv

    # twitterの認証情報を入力
    CONSUMER_KEY = "*****"
    CONSUMER_SECRET = "*****"
    ACCESS_KEY = "*****"
    ACCESS_SECRET = "*****"
    api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

    # xml_parserのget_weather_***で取得した天気情報についてTweetする
    url = 'http://www.drk7.jp/weather/xml/'
    area = param[1]
    date = param[2]

    today = datetime.date.today() #今日
    str_today = str(today.year) + '/' + str(today.month).zfill(2) + '/' + str(today.day).zfill(2)
    name_today = '今日' + str(today.year) + '年' + str(today.month).zfill(2) + '月' + str(today.day).zfill(2) + '日'
    message_today = 'おはようございます！' + predict_weather(url, area, str_today, name_today)

    print message_today

    tomorrow = datetime.date.today() + datetime.timedelta(days = 1) #明日
    str_tomorrow = str(tomorrow.year) + '/' + str(tomorrow.month).zfill(2) + '/' + str(tomorrow.day).zfill(2)
    name_tomorrow = '明日' + str(tomorrow.year) + '年' + str(tomorrow.month).zfill(2) + '月' + str(tomorrow.day).zfill(2) + '日'
    message_tomorrow = predict_weather(url, area, str_tomorrow, name_tomorrow)

    print message_tomorrow

    if date == 'today' :
        api.update_status(status = message_today)
    elif date == 'tomorrow' :
        api.update_status(status = message_tomorrow)