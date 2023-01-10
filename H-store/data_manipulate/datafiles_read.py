import os
from AudioRead import AudioStore
from GraphRead_code import GraphStore
from TSdataRead import TSStore
from KVdataRead import vedioStore
import pickle as pkl
'''
    Read all files in the user-defined file directory!
'''
# 获取本地的数据
File_directory = '/Scode3/H-Store/DATA/'
files= os.listdir(File_directory)



# 上传的文件的完整路径,由两部分组成
# File_dir 第一部分是到文件夹的路径
# file 第二部分是文件的具体名字
def DataRead(File_dir,file):
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
          if  os.path.splitext(file)[-1] in ['.wav','.mp3']:
               AudioStore(File_dir,file)
          elif os.path.splitext(file)[-1] in ['.gexf']:
               GraphStore(File_dir,file)
          elif os.path.splitext(file)[-1] in ['.json',]:
               TSStore(File_dir,file)
          else:
               vedioStore(File_dir,file)
               
if __name__ == "__main__":
     pkl