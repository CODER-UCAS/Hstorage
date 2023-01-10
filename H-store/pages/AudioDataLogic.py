import streamlit as st
# import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
import networkx as nx
from PIL import Image
import pickle as pkl
import sys
sys.path.append("/Scode/H-Store/data_manipulate/")#/TSdataRead.py
# sys.path.append("/Scode/H-Store/data_manipulate/datafiles_read.py")
# print(sys.path)
from datafiles_read import DataRead
from TSdataRead import dataRead,dateTovalue
from AudioRead import AudiodataRead
from GraphRead_code import GraphStore,GraphRead,deleteRelation,AddRelation
from KVdataRead import Search4Key,Delete4Key,Update4key,Search_All


def GetSpeedData(data_name):
    # File_directory = '/Scode/H-Store/'
    # DataRead(File_directory)
    data = AudiodataRead(data_name)
    # st.text(data)
    # times = []
    # values = []
    # for k,v in data.items():
    #     times.append(k)
    #     values.append(v)
    df = pd.DataFrame(data)
    return df,data

def SpeedData(name = 'N'):
    # load = 0
    st.markdown("您现在查询的是 语音数据 ")
    datasets = find_cls_in_pkl("语音数据")
    data_name = st.selectbox("您想要查询的数据集是",[i for i in datasets])#,label_visibility = 'collapsed'
    df,dict_data = GetSpeedData(data_name)
    # fig, ax = plt.subplots(figsize = (4, 3))
    # # fig
    # ax.plot(df['date'],df['values'])
    # st.pyplot(fig)
    
    func = st.selectbox("您想要进行的操作是",['展示','查询'])#,label_visibility = 'collapsed'
    if func == '展示':
        # st.markdown(df)
        with st.form('example form') as f:
            ag = AgGrid(
                df,
                editable=True,
                height=250,
                fit_columns_on_grid_load=True,
                reload_data=False
            )
            st.form_submit_button('🥰')
            
    else:
        time_search = st.text_input("请输入查询的times，格式如20: ")# if time_search :
        #     st.markdown(time_search)
        # st.write('The current number is ', time_search)
        if time_search:
            df_1 = df[df['times'] == time_search]['values'].values[0]
            st.text(f"{time_search}: " + df_1)