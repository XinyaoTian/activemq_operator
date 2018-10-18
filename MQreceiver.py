from funcPackage.MQOperator import MQOperator

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    mqOperator = MQOperator("./MQOperator_conf.json")
    logging.info("The receiver of MQOperator has been opend.")
    while True :
        mqOperator.receiveFromQueue()
