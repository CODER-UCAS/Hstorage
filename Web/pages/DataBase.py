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

File_directory = '/Scode/H-Store/DATA/'

st.set_page_config(page_title="DataBase",
                layout='wide',
                page_icon="📈")

# def search_data(search_item):
#     # return "deploy some data you are searching"
#     return classifier_database('时序数据').iloc[0:1]

# def delete_data():
#     pass

# @st.cache
# def classifier_database(data_name):
#     return pd.DataFrame(
#    np.random.randn(50, 5),
#    columns=('col %d' % i for i in range(5)))

def find_cls_in_pkl(cls):
     f_read = open('../H-Store/DATA/dict_file.pkl', 'rb')
     dict_pkl = pkl.load(f_read)
     print(dict_pkl)
     f_read.close()
     return dict_pkl[cls]
    
#------------------------------------------------
# @st.cache
# def TDR():
#     File_directory1 = '/Scode/H-Store/ts/'
#     DataRead(File_directory1)

# @st.cache
# def GDR():
#     GraphStore('/Scode/H-Store/graph/','382.gexf')
#------------------------------------------------

def tuplestr2int(edge_lists):
    for i in range(len(edge_lists)):
        edge_lists[i] = (int(edge_lists[i][0]),int(edge_lists[i][1]))
    return edge_lists

def str2int(node_lists):
    for i in range(len(node_lists)):
        node_lists[i] = int(node_lists[i])
    return node_lists

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
    
def GetGraphData():
    # GDR()
    node_lists,edge_lists = GraphRead()
    # node_lists = node_lists
    # print(node_lists,edge_lists)
    # print("----------")
    # print(node_lists,edge_lists)
    graph = nx.Graph()
    # graph.add_nodes_from(node_lists)
    graph.add_edges_from(edge_lists)
    return graph

def draw(graph):
    nx.draw(graph, with_labels=True, alpha=0.8, node_size=500)
    plt.savefig("./pic/graph_pic.jpg")
    plt.show()
    image = Image.open("./pic/graph_pic.jpg")
    st.image(image,caption='图数据')

def GraphData():
    # er = nx.erdos_renyi_graph(10, 0.15)
    graph = GetGraphData()
    print(graph.nodes,graph.edges)
    # draw(graph)
    # plt.figure(dpi = 150)
    # print(graph.nodes)
    func = st.selectbox("您想要进行的操作是",['展示','删除','添加'])#,label_visibility = 'collapsed'
    if func == '展示':
        draw(graph)
        
    if func == '删除':
        st.markdown("请输入两个节点来删除对应的边：")
        node1 = st.text_input("请输入一个节点")
        node2 = st.text_input("请输入另一个节点")
        delete = st.button("确定")
        if delete:
            print(node1,node2)
            deleteRelation(str(node1),str(node2))
    if func == '添加':
        st.markdown("请输入两个节点来添加对应的边：")
        node1 = st.text_input("请输入一个节点")
        node2 = st.text_input("请输入另一个节点")
        add = st.button("确定")
        if add:
            AddRelation(str(node1),str(node2))
    if func != '展示':
        if st.button("刷新图数据"):
            draw(graph)

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

# def SpeedData(name = 'N'):
#     # load = 0
#     st.markdown("您现在查询的是 语言数据 ")
#     datasets = find_cls_in_pkl("语音数据")
#     data_name = st.selectbox("您想要查询的数据集是",[i for i in datasets])#,label_visibility = 'collapsed'
#     df,dict_data = GetSpeedData(data_name)
#     st.markdown(df)
#     with st.form('example form') as f:
#         ag = AgGrid(
#             df,
#             editable=True,
#             height=250,
#             fit_columns_on_grid_load=True,
#             reload_data=False
#         )
#         st.form_submit_button('-')
#     time_search = st.text_input("请输入查询的times，格式如20: ")

#     if time_search:
#         df_1 = df[df['times'] == time_search]['values'].values[0]
#         st.text(f"{time_search}: " + df_1)





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
    

def deploy_data():
    # dm = data_manager()


    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    st.sidebar.write(":fire:选择上传的文件")
    # filename = st.sidebar.file_uploader(accept_multiple_files  = True, label = '* 选择添加/上传的文件',label_visibility = 'collapsed')#,label_visibility = 'hidden'
    uploaded_file = st.sidebar.file_uploader(label = '选择文件')
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)
        with open(f"{File_directory}/{uploaded_file.name}", "wb") as f:
            f.write(bytes_data)
        DataRead(File_directory,uploaded_file.name)
        
    
    
    
    
    
    # st.write(filename) 通过filename得到文件名，上传数据的逻辑需要看一下。
    st.sidebar.write(":accept: 请点击你所需要显示的数据库")
    data_frame = st.sidebar.selectbox(" :accept: 请点击你所需要查询的数据库",['时序数据','语音数据','图数据','键值数据'],label_visibility = 'collapsed')
    # df = classifier_database(data_frame)
    # df = dm()

    if data_frame == '时序数据':
        TimeData()
    if data_frame == '语音数据':
        SpeedData()
    if data_frame == '图数据':
        GraphData()
    if data_frame == '键值数据':
        KVData()
    # st.markdown(f"## {data_frame}的数据展示👇")
    # with st.form('example form') as f:
    #     ag = AgGrid(
    #         df,
    #         editable=True,
    #         height=250,
    #         fit_columns_on_grid_load=True,
    #         reload_data=False
    #     )
    #     st.form_submit_button('提交修改')
    # # 通过st.dataframe(ag['data'])获得修改后的数据，需要通过对比找到哪个数据是被修改的。

    # st.write("## 📖查找数据")
    # search_item = st.text_input(label = 'search_data',placeholder = 'input data',label_visibility = 'collapsed')
    # if search_item:
    #     search_result_df = search_data(search_item)
    #     st.markdown("### 查询结果👇🏻")
    #     with st.form('search') as f:
    #         ag = AgGrid(
    #             search_result_df,
    #             editable=True,
    #             height=100,
    #             fit_columns_on_grid_load=True,
    #             reload_data=False
    #         )
    #         col1, col2, _ = st.columns([1,1,4])
    #         with col1:
    #             submit_new_data = st.form_submit_button("提交修改")
    #         with col2:
    #             delete_data_status = st.form_submit_button("提交删除")
    #             if  delete_data_status:
    #                 delete_data()
                    
                    
        # st.success(search_item)
        # if st.button("删除数据"):
        #     delete_data()


def main_ui():
    st.title("🤗数据库操作界面")
    if st.session_state.get("login_status",False):
        st.text(f"🙆🏻‍♀️您已登录成功")
        deploy_data()
    else:
        st.error('🙅🏻‍♀️请先按登录！请点击左边UserInfo进行登录验证！')



main_ui()

# if __name__ == '__main__':
    