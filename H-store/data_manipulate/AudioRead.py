from pydub import AudioSegment
import sys
import os
import wave
import io
import numpy as np
import matplotlib.pyplot as plt   #专业绘图库
from PIL import Image
import pylab
from scipy.io import wavfile
from Storage import DBConnector


def AudioStore(filedir,filename):
    file = filedir+filename

    f = wave.open(filedir+filename,'rb')
    print(file)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    wavaData = np.frombuffer(strData,dtype=np.int32)
    waveData = wavaData*1.0/(max(abs(wavaData)))

    # print(os.path.splitext(filename)[0])

    Pgconn = DBConnector.pgConnect()
    # plot
    time = np.arange(0,nframes)*(1.0/framerate)
    # print(wavaData.size)
    # print(nframes)
    # plt.xlabel("Time(s)")
    # plt.ylabel("Amplitude")
    # plt.title("Single channel wavedata")
    # plt.grid('on') #标尺，on：有，off:无。

    
    cur = Pgconn.cursor()
    str1 = '''DROP TABLE IF EXISTS '''+os.path.splitext(filename)[0]+';'
    print(str1)
    cur.execute(str1)

    string = '''CREATE TABLE '''+os.path.splitext(filename)[0]+'''
      (AudioID  INT  PRIMARY KEY   NOT NULL,
      time           VARCHAR(50)   NOT NULL,
      Data           VARCHAR(50)   NOT NULL);'''
    cur.execute(string)
    print("Table created successfully")
    i=0
    for data in waveData:
        string2 = '''Insert INTO '''+os.path.splitext(filename)[0]+'''(
        AudioID,time,Data) VALUES('''+str(i+1)+''','''+str(data)+''','''+str(time[i])+''');'''
        cur.execute(string2)
        i = i+1

    print("Table created successfully,"+str(i)+"entries has been inserted!")

    Pgconn.commit()
    Pgconn.close()

def AudiodataRead(filename):

    dict ={}

    times = []
    values = []
    Pgconn = DBConnector.pgConnect()
    str1 = '''SELECT * FROM '''+filename+''';''' 
    cur = Pgconn.cursor()
    cur.execute(str1)
    rows = cur.fetchall()
    for row in rows:
        times.append(row[1])
        print(row[1])
        values.append(row[2])
        print(row[2])
    
    dict['times'] = times
    dict['values'] = values
    Pgconn.commit()
    # 关闭数据库连接
    cur.close()
    Pgconn.close()

    return dict

# 修改数据
# name TS1 TS2
# date 字典的第一个key
# new_vaue 修改后的值
def dateTovalue(name,date,new_value):
    influxconn = DBConnector.influxConnect()
    influxconn.query('drop measurement '+name+';')
    TimeSeriesData[date] = new_value
    print(TimeSeriesData)
    w_json = [{
          "measurement": name,
             "fields": TimeSeriesData
             }]
    
    influxconn.write_points(w_json)

AudiodataRead('audio1')