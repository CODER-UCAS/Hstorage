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