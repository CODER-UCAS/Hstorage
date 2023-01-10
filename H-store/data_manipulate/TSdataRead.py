import networkx as nx
import matplotlib.pyplot as plt
from Storage import DBConnector
import os
import json

TimeSeriesData = {}

def TSStore(filedir,filename):
    dict = {}
    global TimeSeriesData
    with open(filedir+filename, 'r') as fcc_file:
        fcc_data = json.load(fcc_file)
        for val in fcc_data['TimeSeries data']:
            dict[val['timestamp']] = val['value']
        
    influxconn = DBConnector.influxConnect()

    tablename = os.path.splitext(filename)[0]
    TimeSeriesData[tablename] = dict
    w_json = [{
         "measurement": tablename,
            "fields": dict
            }]


    influxconn.write_points(w_json)
    
# 读数据
# 传入文件名如 TS1 TS2 TS3 这样的名字
# 返回一个字典，key是日期，value是 值

def dataRead(filename):
    dict1 = {}
    global TimeSeriesData
    dict1 = TimeSeriesData[filename]
    influxconn = DBConnector.influxConnect()
    result = influxconn.query('select * from '+filename+';') 
    print("Result: {0}".format(result))
    
    return dict1

# 修改数据
# name TS1 TS2
# date 字典的第一个key
# new_vaue 修改后的值
# def dateTovalue(name,date,new_value):
#     print("--------------------------------")
#     print(name,date,new_value)
#     influxconn = DBConnector.influxConnect()
#     influxconn.query('drop measurement '+name+';')
#     TimeSeriesData[name][date] = new_value
#     print(TimeSeriesData)
#     w_json = [{
#           "measurement": name,
#              "fields": TimeSeriesData
#              }]
#     print(w_json)
#     influxconn.write_points(w_json)

def dateTovalue(name,data):
    
    influxconn = DBConnector.influxConnect()
    influxconn.query('drop measurement '+name+';')


    w_json = [{"measurement": name,"fields": data}]
    
    influxconn.write_points(w_json)

