#coding:utf-8
import dbi
import sys
import re
doc="""Usage:
python3 """+__name__+""" -h         显示本条消息
python3 """+__name__+""" [word]     查词
python3 """+__name__+""" -f [file]  导入词典
"""
if __name__=='__main__':
    d=dbi.DataBase()
    if len(sys.argv)==2:
        result= d.find({'word':sys.argv[1]}) or \
                d.find({'explain':{'$regex':r'\r\n'+sys.argv[1]+r'\W\r'}}) or \
                d.find({'word':{'$regex':'^'+sys.argv[1]}}) or \
                d.find({'explain':{'$regex':r'\W'+sys.argv[1]+r'\W'}}) or \
                d.find({'word':{'$regex':sys.argv[1]}}) or \
                d.find({'explain':{'$regex':sys.argv[1]}}) 
 #找到单词 or #找到派生 or #单词前缀匹配 or #解析中出现 #单词部分匹配 #解析部分匹配
        if result:
            print(result['word']+'\n'+result['explain'])
        else:
            print("404 Word not Found !")
    elif len(sys.argv)==3 and sys.argv[1]=='-f':
        d.tload(sys.argv[2])
    elif  len(sys.argv)==1 or sys.argv[1]=='-h':
        print(doc)
    elif len(sys.argv)==3 and sys.argv[1]=='-o':
        d.dump(sys.argv[2])
    elif len(sys.argv)==3 and sys.argv[1]=='-j':
        d.jload(sys.argv[2])
