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

def KVData():
    
    st.markdown("您现在查询的是 键值数据 ")
    datasets = find_cls_in_pkl("键值数据")
    data_name = st.selectbox("您想要查询的数据集是",[i for i in datasets])#,label_visibility = 'collapsed'
    
    func = st.selectbox("您想要进行的操作是",['展示','查找','删除','更新'])#,label_visibility = 'collapsed'
    if func == '展示':
        dict_to_show = Search_All()
        dict_change = dict()
        for k,v in dict_to_show.items():
            dict_change[k] = ','.join(v)
            # dict_to_show
        # [str(i)+]
        # st.text()
        # # df_idx = []
        # for key in range(1,6):
        #     v = Search4Key(data_name,str(key))
        #     print(key,v)
        #     # st.text()
        #     print(type(v))
        #     dict_to_show[key] = v
            # df_idx.append(df_idx)
        # df = pd.DataFrame(dict_change)
        st.json(dict_change)
        # with st.form('example form') as f:
        #     ag = AgGrid(
        #         df,
        #         editable=True,
        #         height=200,
        #         fit_columns_on_grid_load=True,
        #         reload_data=False
        #     )
        #     st.form_submit_button('🥰')
        # st.table(df)
    if func == '查找':
        key = st.text_input("请输入一个键值")
        check = st.button("确定")
        if check:
            st.text(Search4Key(data_name,key))
        
    if func == '删除':
        key = st.text_input("请输入需要删除的键值")
        check = st.button("确定")
        if check:
            Delete4Key(data_name,key)
    if func == '更新':
        key = st.text_input("请输入需要更改的键值")
        value = st.text_input("请输入更改后的值")
        check = st.button("确定")
        if check:
            value = value.replace("[","").replace("]","").replace("'","")
            value = value.split(",")
            update_str = ""
            for i in value[:-1]:
                update_str = update_str + i + '\t'
            update_str = update_str + value[-1]
            print("v is ",update_str)
            Update4key(data_name,key,update_str)