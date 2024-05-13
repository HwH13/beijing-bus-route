# coding=utf-8
import time
import requests
import pandas as pd
import json
import math
import re
import sys

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


# %%
def gcj02towgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


# %%

# 坐标转换计算参数
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


def mycode( cityname, city, key):
    '''
    高德地图依据关键词来检索公交路线，例如设置关键词为1，将会返回所有与1路相关的公交路线，例如：
    1路、兴1路、昌1路等，以及部分与1路无关的路线。故设置k值范围，从0-999，检索出所有的公交路线。
    但由于单个账号1日只能访问100次，所以k的循环次数要在100以内，完成一个城市的公交路线检索需使用
    多个账号或是耗费多日分配查询。
    相关网页：
    https://lbs.amap.com/api/webservice/guide/api-advanced/bus-inquiry 中的公交线路关键词查询
    '''

    for k in range(0, 100):
        print(k)
        time.sleep(1)
        keyword = k
        data_save = {}
        data_save_df = pd.DataFrame(data_save)

        trans_site = []
        rt = {}
        url = 'https://restapi.amap.com/v3/bus/linename?extensions=base&keywords={}&offset=100&city={}&page=1&key={}'.format(
            keyword, cityname, key)

        r = requests.get(url).text
        rt = json.loads(r)

        if len(rt["buslines"]) == 0:

            continue
        else:
            for i in rt['buslines']:
                if i['type'] != "地铁":
                    busline_name = i['name']  # 公交线路名
                    busline_name = validateTitle(busline_name)
                    polyline_site = i['polyline']
                    polyline_site = polyline_site.split(";")
                    for j in range(len(polyline_site)):
                        x_site, y_site = polyline_site[j].split(",")
                        x_site = float(x_site)
                        y_site = float(y_site)
                        trans_site.append(gcj02towgs84(x_site, y_site))

                    data_save_df.loc[0, '城市编码'] = cityname
                    data_save_df.loc[0, '高德地图公交唯一编码'] = i['id']
                    try:
                        data_save_df.loc[0, '线路类型'] = i['type']
                    except:
                        data_save_df.loc[0, '线路类型'] = 0
                    data_save_df.loc[0, '线路名称'] = i['name']
                    data_save_df.loc[0, '路线经纬度'] = str(trans_site)
                    data_save_df.to_csv( './{}_{}公交路线轨迹.csv'.format(city, busline_name), index=False,
                                        encoding='utf-8-sig')
                else:
                    continue
    sys.exit()

if __name__ == '__main__':
    city = "北京"
    cityname = '110000'         #高德地图城市的唯一编码
    key = ''                    #key在高德api中申请，注册的key是web端服务，不是web JSAPI!

    mycode( cityname, city, key)
