# -*- encoding:utf-8 -*-
from funcPackage.MQOperator import MQOperator

import logging
logging.basicConfig(filename='./logs/MQreceiver.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', filemode='w',level = logging.ERROR,datefmt='%Y-%m-%d %I:%M:%S %p')

if __name__ == "__main__":
    mqOperator = MQOperator("./MQOperator_conf.json")
    logging.info("The receiver of MQOperator has been opend.")
    print("MQOperator started.")
    # 使其作为一个监听服务启动
    while True :
        mqOperator.receiveFromQueue()
