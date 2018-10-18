# -*- encoding:utf-8 -*-
import json
import logging
# 注意 这里写的日志打印路径是在运行 MQreceiver.py 时 系统的pwd
logging.basicConfig(filename='../logs/MQreceiver.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', filemode='w',level = logging.ERROR,datefmt='%Y-%m-%d %I:%M:%S %p')


# 读取默认位置的配置文件 特别注意测试和运行时刻的工作路径!
def get_conf(file_path="../MQOperator_conf.json"):
    try:
        return get_json(file_path)
    except:
        logging.error("Configration file can not be loaded. (file_path = %s)" % file_path)
        raise IOError

# 读取json格式的文件，返回一个dict类型
def get_json(file_path):
    try:
        with open(file_path,'r')as f:
            temp = json.loads(f.read())
        f.close()
        return temp
    except:
        logging.error("json format in this file is not correct. (file_path = %s) " % file_path)
        raise IOError


if __name__ == "__main__":
    print get_conf()