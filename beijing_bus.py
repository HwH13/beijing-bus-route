#方向生成问题已解决，但未爬取反向数据
import requests
import pandas as pd
import json
import math
#%%
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
    return lng * 2 - mglng, lat * 2 - mglat
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
#%%
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

path = "Network_bus.txt"
cityname = '北京'
fangxiang = 0

with open(path, "r") as f:
    for xm in f.readlines():
        xm = xm.replace('\n', '').replace("['",'').replace("']","").replace("'","")
xm = xm.split(',')
nodata = []
for k in range(len(xm)-1):
    dt = {}
    station_name = []
    station_coords = []
    a1 = 0
    b1 = 0
    tmp={}
    xin = []
    rt = {}
    aarray = []
    barray = []
    line = xm[k]
    url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=a5b7479db5b24fd68cedcf24f482c156&output=json&city={}&offset=0&keywords={}&platform=JS'.format(cityname,line)
    r = requests.get(url).text
    rt = json.loads(r)
    try:
        for st in rt['buslines'][fangxiang]['busstops']:
            station_name.append(st['name'])
            station_coords.append(st['location'])
    except:
        print('没有{}路公交'.format(line))
        nodata.append(xm[k])
        continue
    polyline=rt['buslines'][fangxiang]['polyline']
    polyline=polyline.split(";")
    tmp['station_coords']=polyline
    for j in range(len(polyline)):
        xx,yy = polyline[j].split(",")
        xx = float(xx)
        yy = float(yy)
        xin.append(gcj02towgs84(xx,yy))
    path=pd.DataFrame(tmp)
    dm = pd.DataFrame(dt)
    for i in range(len(station_name)-1):
        zanshi = ()
        dm.loc[i,'line_name'] = rt['buslines'][fangxiang]['name']
        xiabiao_q = dm.loc[i, 'line_name'].rfind('(')
        Line_name = dm.loc[i, 'line_name'][:xiabiao_q]
        Fangxiang = dm.loc[i, 'line_name'][xiabiao_q + 1:-1]
        dm.loc[i, 'line_name'] =Line_name
        dm.loc[i,'fangxiang'] = Fangxiang
        dm.loc[i,'station_name1']=station_name[i]
        dm.loc[i,'station_name2']=station_name[i+1]
        dm.loc[i,'qj']=station_name[i] + '_' + station_name[i+1]
        try: #若有点重复，选index大的点
            a1,b1=path.index[path.station_coords.isin([station_coords[i],station_coords[i+1]])]
        except:
            acunchu =path.index[path.station_coords.isin([station_coords[i]])]
            bcunchu =path.index[path.station_coords.isin([station_coords[i+1]])]
            a1 = acunchu[len(acunchu)-1]
            b1 = bcunchu[len(bcunchu)-1]
        for s in range(a1,b1+1):
            xin[s] = str(xin[s])
            xin[s] = xin[s].replace('(','')
            xin[s] = xin[s].replace(')','')
            zanshi += (xin[s],)
        str1 = '],['.join(zanshi)
        str1 ="[[" + str1 + "]]"
        dm.loc[i,'coords'] = str1
    dm.to_csv('正向北京公交\{}{}公交路线轨迹.csv'.format(cityname,line),index=False,encoding='utf-8-sig')
f1 = open("nodata.txt","w")
f1.write(str(nodata))
f1.close()










