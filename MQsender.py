from funcPackage.MQOperator import MQOperator

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    mqOperator = MQOperator("./MQOperator_conf.json")
    logging.info("The testisender of MQOperator has been create.")
    # mqOperator.sendToQueue('{"type":"setup","userID":"mike0501","timestamp":"20180909","image":"nginx","image_version":"latest","port":"[80]"}')
    mqOperator.sendToQueue(
        '{"type":"setup","deploy_name":"jupyter-mikey-0802","userID":"mike0501","timestamp":"20180909","image":"jupyter/minimal-notebook","image_version":"latest","port":"[8080]"}')
