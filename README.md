1 代码功能
=
beijing_bus.py 通过高德地图api中的公交线路信息关键词查询，获取北京所有公交线路信息，信息包括：线路名、方向、沿路的经纬度，接口的说明网址：https://lbs.amap.com/api/webservice/guide/api-advanced/bus-inquiry。 

2 运行输入及输出
=
2.1 beijing_bus.py
-
输入：

**city**参数为带访问的城市中文名，输出文件中会带有此名称。

**cityname**参数为待访问的城市编码（由高德定义，可在网址*https://lbs.amap.com/api/webservice/guide/api-advanced/bus-inquiry*中公交信息查询模块找到）。

**key**参数为访问接口的个人信息标注，在高德api-控制台-应用-key 中查询，注意，这个key是web端服务的，不是webJSapi！单人每日仅能访问接口100次！。

**k**程序77行的k为查询公交的关键词范围，例如要查询0路-100路之间的所有公交，设置范围为0-100。

输出：

查询到的数据会输出到**对应线名的csv文件中**。


3 程序运行
=

beijing_bus.py程序不可直接运行，须在高德api中获取key值，填入代码中对应地方才可运行，以获得各线路的途径站及经纬度坐标。







> Written with [StackEdit](https://stackedit.io/).
