import json
import requests
import os
from script.locate import *

def jsondir():
    os.chdir(os.getcwd())
    dir = os.getcwd() + "/json/"
    if not os.path.exists(dir):
        os.mkdir(dir)
        
def deletejson(name):
    jsondir()
    full_name = "json/%s.json"%name
    if os.path.exists(full_name):
        os.remove(full_name)

def jsonjudge_auto(name):
    jsondir()
    full_name = "%s.json"%name
    if not os.path.exists("json/%s"%full_name):
        return_json = download_json("%s%s"%(DATA_JSON_LIST, full_name), full_name)
    else:
        print("从本地获取%s..."%full_name)
        return_json = read_json("%s"%full_name)
    return return_json

def read_json(name):
    jsondir()
    if (os.path.exists("json/%s"%name)):
        fjson = open("json/%s"%name, encoding="utf-8", errors='ignore')
        text = fjson.read()
        fjson.close()
        data = json.loads(text)
        return data
    else:
        print("不存在%s!"%name)
        return []

def download_json(url,name):
    jsondir()
    print("正在下载%s..."%name)
    session = requests.session()
    get_result = session.get(url)
    content = get_result.content
    sjson = open("json/%s"%name, 'wb')
    sjson.write(content)
    sjson.close()
    result = content.decode("utf-8",errors="ignore")
    try:
        json_test = json.loads(result)
        print("解析%s成功，json文件长度为%d" % (name,len(result)))
        return json_test
    except:
        print("解析%s出现错误，json文件长度为%d" % (name, len(result)))
        return []