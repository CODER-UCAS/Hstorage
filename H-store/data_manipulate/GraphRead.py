import networkx as nx
import matplotlib.pyplot as plt
from Storage import DBConnector
import os
import random
from py2neo import *
import pandas as pd

graphconn = DBConnector.GraphConnect()
edgelists = []
nodelists = []

def GraphStore(filedir,filename):
	
    nodes = {}
    edges = []
    global graph
    
    graphconn.delete_all()
    graphdata = nx.read_gexf(filedir+filename)    
    global edgelists
    global nodelists

    edgelists = list(graphdata.edges())
    nodelists = list(graphdata.nodes())

    for node in list(graphdata.nodes()):
        print(node)
        n = Node('Person',name = node, age = random.randint(10,100))
        nodes[node] = n
        graphconn.create(n)
    
    for edge in list(graphdata.edges()):
        n1 = Relationship(nodes[edge[0]], 'test', nodes[edge[1]])
        edges.append(n1) 
        graphconn.create(n1)
    
#
#
def GraphRead():
    global edgelists
    global nodelists
    str = "match(n) RETURN (n)";
    
    # pd.DataFrame(nodes_data)['n'][0]) 
    # for index,row in pd.DataFrame(nodes_data).iterrows(): 
    #     print(type(row)) 
       
    return nodelists,edgelists

def Search4Name(na):
    matcher = NodeMatcher(graphconn)
    nodes = matcher.match('Person', name=na).all()
    nodelist = []
    for node in nodes:
        nodelist.append(node['name'])
    return nodelist

def UpdateNode(na,new_name):
    tx = graphconn.begin()
    matcher = NodeMatcher(graphconn)
    init_node = matcher.match("Person", name=na)
    new_node = init_node.first()
    new_node['name'] = new_name
    sub = Subgraph(nodes=[new_node])
    tx.push(sub)
    tx.commit()


def AddRelation(n1,n2):
    matcher = NodeMatcher(graphconn)
    node1 = matcher.match('Person', name=n1).first()
    node2 = matcher.match('Person', name=n2).first()

    relation = Relationship(node1,'NewRelation', node2)


    global edgelists
    global nodelists

    edgelists.append((node1['name'],node2['name']))
    graphconn.create(relation)

def deleteRelation(n1,n2):
    matcher = NodeMatcher(graphconn)
    r_matcher = RelationshipMatcher(graphconn)
    node1 = matcher.match('Person', name=n1).first()
    node2 = matcher.match('Person', name=n2).first()

    global edgelists
    for idx,(i,j) in enumerate(edgelists):
        if i == node1['name'] and j == node2['name'] :
            del edgelists[idx]
            break

    relation = r_matcher.match(nodes=[node1, node2]).first()

    graphconn.delete(relation)


# GraphStore('/Scode/H-Store/graph/','382.gexf') #执行一次就好
# GraphRead() #读所有数据，返回两个列表 
# deleteRelation('0','1') #删除一个关系

# AddRelation('2','3') #添加一个关系
