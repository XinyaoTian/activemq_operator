# -*- encoding:utf-8 -*-
import json

# 读取默认位置的配置文件
def get_conf(file_path="../MQOperator_conf.json"):
    return get_json(file_path)

# 读取json格式的文件，返回一个dict类型
def get_json(file_path):
    configrations_dict = {}
    with open(file_path,'r')as f:
        temp = json.loads(f.read())
    f.close()
    return temp

print get_conf()