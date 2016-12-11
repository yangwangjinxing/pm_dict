# pmDict
    Dict using python and mongodb

## version 0.1

## Usage

    python3 dict.py -h          帮助信息
    pyhton3 dict.py -f [file]   导入数据
    python3 dict.py [word]      查词

## 数据格式

txt格式：

    word
    / w\:d; w[d/解释...
    解释...
    ...
Json格式：

    {'word':'foo','explain':"foo"}
    [{'word':'foo','explain':"foo"},...]

Change Log

    支持部分匹配
