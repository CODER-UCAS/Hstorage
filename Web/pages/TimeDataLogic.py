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


def GetTimeData(data_name):
    # TDR()
    data = dataRead(data_name)
    times = []
    values = []
    for k,v in data.items():
        times.append(k)
        values.append(v)
    df = pd.DataFrame({'date':times,'values':values})
    return df,data



def TimeData(name = 'N'):
    # load = 0
    st.markdown("您现在查询的是 时序数据 ")
    datasets = find_cls_in_pkl("时序数据")
    data_name = st.selectbox("您想要查询的数据集是",[i for i in datasets])#,label_visibility = 'collapsed'
    df,dict_data = GetTimeData(data_name)
    # fig, ax = plt.subplots(figsize = (4, 3))
    # # fig
    # ax.plot(df['date'],df['values'])
    # st.pyplot(fig)
    
    func = st.selectbox("您想要进行的操作是",['展示','修改'])#,label_visibility = 'collapsed'
    if func == '展示':
        # st.markdown(df)
        plt.plot(df['values'][:50])
        plt.savefig("./pic/time_pic.jpg")
        plt.show()
        image = Image.open("./pic/time_pic.jpg")
        st.image(image,caption=f'{data_name}部分数据可视化')
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
        time_search = st.text_input("请输入查询的时间，格式如'1981-01-02': ")
        # if time_search :
        #     st.markdown(time_search)
        # st.write('The current number is ', time_search)
        if time_search:
            df_1 = df[df['date'] == time_search]['values'].values[0]
            st.text(f"{time_search}: " + df_1)
            values_change = st.text_input("修改数值为：")
            dict_data[time_search] = values_change
                
            if values_change:
                dateTovalue(data_name,dict_data)