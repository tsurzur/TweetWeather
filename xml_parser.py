#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom
import urllib2

# url 天気予報サイト(http://www.drk7.jp/weather/xml/)
# s_area: 指定地域（兵庫県南部 or 大阪府）
# s_date: 指定日付（現在から５日後まで）
def set_weather_info(url, s_area, s_date):
    # sitemap.xmlを取得する
    if s_area == '兵庫県南部':
        area_label = 28
    elif s_area == '大阪府':
        area_label = 27
    elif s_area == '東京都':
        area_label = 13

    prefacture_xml = urllib2.urlopen(url + '/' + str(area_label) + '.xml').read()
    file_xml = minidom.parseString(prefacture_xml)

    # 指定エリアの情報を取得
    info_area = file_xml.getElementsByTagName('area')
    for i, area in enumerate(info_area) :
        id = area.getAttribute('id')
        if id == '南部' or id == '大阪府' or id == '東京地方' :
            print 'AREA:' + id
            dst_area = area
            break

    # 指定日付の情報を取得
    info_date = dst_area.getElementsByTagName('info')
    for i, date in enumerate(info_date) :
        day = date.getAttribute('date')
        if day == s_date :
            print 'DATE:' + day
            dst_date = date
            break

    return dst_date

def get_rain_fall_chance(date):
    list_weather_rain = []
    info_rain_fall_chance = date.getElementsByTagName('period')
    for i, chance in enumerate(info_rain_fall_chance) :
        hour = chance.getAttribute('hour')
        # print hour + ' = ' + chance.childNodes[0].data
        list_weather_rain.append(chance.childNodes[0].data)

    return list_weather_rain

def get_weather_name(date):
    info_weather_name = date.getElementsByTagName('weather')[0]
    return info_weather_name.childNodes[0].data
