#coding:utf-8
import dbi
import sys
import re
doc="""Usage:
python3 """+__name__+""" [word]     查词
python3 """+__name__+""" -h         显示本条消息
python3 """+__name__+""" -f [file]  导入txt
python3 """+__name__+""" -j [file]  导入json
python3 """+__name__+""" -o [file]  导出json
"""


def youdao_trans(word):
    import requests
    from lxml import etree
    xpath = '//*[@id="results-contents"]//text()'
    urlp = 'http://youdao.com/w/eng/%s'
    url = urlp % word
    r = requests.get(url, timeout=1)
    root = etree.HTML(r.text)
    texts = root.xpath(xpath)
    texts = [t.strip() for t in texts if t.strip()]
    return ' '.join(texts)


if __name__=='__main__':
    d=dbi.DataBase()
    if len(sys.argv)==2:
        result= d.find({'word':{'$regex':r'^'+sys.argv[1]+r'$','$options':'$i'}}) or \
                d.find({'explain':{'$regex':r'\r\n'+sys.argv[1]+r'\W\r','$options':'$i'}}) or \
                d.find({'word':{'$regex':'^'+sys.argv[1],'$options':'$i'}}) or \
                d.find({'explain':{'$regex':r'\W'+sys.argv[1]+r'\W','$options':'$i'}}) or \
                d.find({'word':{'$regex':sys.argv[1],'$options':'$i'}}) or \
                d.find({'explain':{'$regex':sys.argv[1],'$options':'$i'}})
 #找到单词 or #找到派生 or #单词前缀匹配 or #解析中出现 #单词部分匹配 #解析部分匹配
        if result:
            print(result['word']+'\n'+result['explain'])
        else:
            print("Not found at local, searching at youdao...")
            try:
                print(youdao_trans(sys.argv[1]))
            except Exception as e:
                print('fail with %s', e)
    elif len(sys.argv)==3 and sys.argv[1]=='-f':
        d.tload(sys.argv[2])
    elif  len(sys.argv)==1 or sys.argv[1]=='-h':
        print(doc)
    elif len(sys.argv)==3 and sys.argv[1]=='-o':
        d.dump(sys.argv[2])
    elif len(sys.argv)==3 and sys.argv[1]=='-j':
        d.jload(sys.argv[2])
