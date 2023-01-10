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
import leveldb

datum = {}

# 存储文件
def vedioStore(filedir,filename):
	dict = {}
	db=leveldb.LevelDB("./"+os.path.splitext(filename)[0])
	global datum
	with open(filedir+filename, mode="r") as file:
		list = file.readlines()
		for row in list:
			l = row.split('\t',1)
			db.Put(bytes(l[0],encoding='utf-8') ,bytes(l[1],encoding='utf-8'))
			dict[l[0]] = l[1]
			str1 = l[1].split('\t')
			datum[l[0]] = str1

# 根据key查看数据，返回一个数据的list
def Search4Key(tablename, key):

	db=leveldb.LevelDB("./"+tablename)
	bytes1 = db.Get(bytes(key,encoding='utf-8'))

	str1 = str(bytes1,encoding='utf-8')

	list = str1.split('\t')
	

	print(list)
	return list

#根据key删除数据
def Delete4Key(tablename, key):

	global datum	

	db=leveldb.LevelDB("./"+tablename)

	bytes1 = db.Delete(bytes(key,encoding='utf-8'))

	del datum[key] 

#根据key更新数据，参数是一个字符串
def Update4key(tablename, key,new_value):
	global datum

	db=leveldb.LevelDB("./"+tablename)
	db.Delete(bytes(key,encoding='utf-8'))

	db.Put(bytes(key,encoding='utf-8') ,bytes(new_value,encoding='utf-8'))

	datum[key] = new_value

def Search_All():
	global datum
	return datum

a = '/Scode3/H-Store/vedio/'
vedioStore(a,"vedio1.mp4")

if __name__ == '__main__':
	pass
	# Search4Key(TAB1,'80')