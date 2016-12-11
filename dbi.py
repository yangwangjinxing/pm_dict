#coding:utf-8
from pymongo import MongoClient
from functools import wraps
import json

def log(func):
    @wraps(func)
    def _log(*args,**kwargs):
        print(func.__name__+' runing')
        func(*args,**kwargs)
        print(func.__name__+' exit')
    return _log

class DataBase(object):
    def __init__(self,db='dict',host='localhost',port=27017):
        self.db=MongoClient(host,port)[db]
    def add(self,dict_,coll='ox'):  #dict_传入为引用
        self.db[coll].insert(dict_)  
    def find(self,dict_,coll='ox'):
        return self.db['ox'].find_one(dict_)

    @log
    def tload(self,path):
        with open(path,"r") as f:
            dict_={'word':'','explain':''}
            buf=['','',1]
            l=open('log.txt','w')
            while buf[2]:
                buf[2]=f.readline()
                if  not buf[2] or buf[2][0]=='/':
                    dict_['explain']=buf[0]
                    if(dict_['word']):
                        l.writelines(dict_['word'])
                        dict_['word']=dict_['word'][0:-2]    #remove \r\n
                        self.add(dict_)
                        del dict_['_id']    #插入之后dict会增加一个_id字段
                    dict_['word']=buf[1]
                    buf[0]=buf[2]
                    buf[1]=""
                else:
                    buf[0]+=buf[1]
                    buf[1]=buf[2]
            l.close()
    @log
    def jload(self,path):
        with open(path,'r') as f:
            self.add(json.loads(f.read())
)
    @log
    def dump(self,path):
        with open(path,"w") as f:
            l=[]
            for i in self.db['ox'].find():
                del i['_id']
                l.append(i)
            f.writelines(str(json.dumps(l)))
