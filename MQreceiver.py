from funcPackage.MQOperator import MQOperator

import logging
logging.basicConfig(filename='./logs/MQreceiver.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', filemode='w',level = logging.ERROR,datefmt='%Y-%m-%d %I:%M:%S %p')

if __name__ == "__main__":
    mqOperator = MQOperator("./MQOperator_conf.json")
    logging.info("The receiver of MQOperator has been opend.")
    while True :
        mqOperator.receiveFromQueue()
