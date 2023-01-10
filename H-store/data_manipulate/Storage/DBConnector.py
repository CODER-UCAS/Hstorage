import psycopg2 ##导入
import leveldb
import py2neo
from py2neo import Graph
from influxdb import InfluxDBClient

'''
    PostgreSQL connector module
'''
def pgConnect():
    conn = psycopg2.connect(database="hstore", user="postgres", password="postgres", host="127.0.0.1", port="5432")
    print('PostgreSQL connection successful!')
    return conn

'''
    LevelDB connector module
'''
def leveldbConnect():
    db = leveldb.LevelDB("hstore");
    print('LevelDB connection successful!')
    return db

def GraphConnect():
    graph = Graph('bolt://localhost:7687',auth=("neo4j", "RuanGong11"))
    print('Neo4j connection successful!')
    return graph


def influxConnect():
    conn = InfluxDBClient('localhost','8086','h1','RuanGong11','hstore')
    print('InfluxDB connection successful!')
    return conn


