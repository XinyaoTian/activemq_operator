# -*- encoding:utf-8 -*-
import stomp
import time
from datetime import datetime
from K8sOperator import K8sOperator
import logging
# 注意 这里写的日志打印路径是在运行 MQreceiver.py 时 系统的pwd
logging.basicConfig(filename='./logs/MQreceiver.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', filemode='w',level = logging.ERROR,datefmt='%Y-%m-%d %I:%M:%S %p')

import os

from json_reader import get_conf

# Listener 类 ; 根据官方文档书写，作为监听ActiveMQ队列的对象
class Listener(stomp.ConnectionListener):
    # 从ActiveMQ中接收到消息时的动作 这个函数是stomp包 fork一个子进程去执行的 因此可以并发
    def on_message(self, headers, message):
        # logging.INFO(str(datetime.now()) + 'headers: %s' % headers)
        # logging.INFO(str(datetime.now()) + 'message: %s' % message)
        print "headers : %s " % headers
        print "message : %s " % message
        # print type(headers)
        # print type(message)
        if headers is not None :
            # Actions after received messages here:
            # ----------- #


            # ----------- #
            pass
        else:
            pass

# 改进的 Listener 类 ，拥有特定的用法 ; 根据官方文档书写，作为监听ActiveMQ队列的对象
class Listener_receive(stomp.ConnectionListener):

    # 从ActiveMQ中接收到消息时的动作 这个函数是stomp包 fork一个子进程去执行的 因此可以并发
    def on_message(self, headers, message):
        # logging.INFO(str(datetime.now()) + 'headers: %s' % headers)
        # logging.INFO(str(datetime.now()) + 'message: %s' % message)
        print "headers : %s " % headers
        print "message : %s " % message
        # print type(headers)
        # print type(message)
        if headers is not None and message is not None:
            print "After eval ,type : %s ; msg : %s" % ( type(eval(message)) , eval(message) )
            # Actions after received messages here:
            # ----------- #
            # 执行传入的命令
            message_dict = eval(message)
            logging.critical("Receive a massage.")
            logging.critical("headers : %s" % str(headers))
            logging.critical("message : %s" % str(message))
            if message_dict.has_key('command') :
                cmd = str(message_dict['command'])
                print cmd
                os.system(message_dict['command'])
            else:
                logging.error("No command in message.")

            # ----------- #
        else:
            pass

# 改进的 Listener 类 ，拥有特定的用法 ; 根据官方文档书写，作为监听ActiveMQ队列的对象
class Listener_k8s(stomp.ConnectionListener):

    # 从ActiveMQ中接收到消息时的动作 这个函数是stomp包 fork一个子进程去执行的 因此可以并发
    def on_message(self, headers, message):
        # logging.INFO(str(datetime.now()) + 'headers: %s' % headers)
        # logging.INFO(str(datetime.now()) + 'message: %s' % message)
        print "headers : %s " % headers
        print "message : %s " % message
        # print type(headers)
        # print type(message)
        if headers is not None and message is not None:
            print "After eval ,type : %s ; msg : %s" % ( type(eval(message)) , eval(message) )
            # Actions after received messages here:
            # ----------- #
            # 执行传入的命令
            message_dict = eval(message)
            logging.critical("Receive a massage.")
            logging.critical("headers : %s" % str(headers))
            logging.critical("message : %s" % str(message))
            # 若这个消息是完整的
            if message_dict.has_key('type') and  message_dict.has_key('userID') \
                    and message_dict.has_key('image') and message_dict.has_key('timestamp')\
                    and message_dict.has_key('image_version') and message_dict.has_key('port') \
                    and message_dict.has_key('deploy_name'):


                #ToDo : 调用K8sCmdFunc.py中的函数来实现功能
                k8s_op = K8sOperator(message_dict['type'], message_dict['deploy_name'],
                                     message_dict['userID'], message_dict['timestamp'],
                                     message_dict['image'], message_dict['image_version'], message_dict['port'])
                # k8s_op.checkAndDoCommandType()
                k8s_op.dealWithJupyter()

                pass

            # 否则，不予执行
            else:
                logging.error("Can not manipulate the message = %s ." % str(message_dict))

            # ----------- #
        else:
            pass



class MQOperator():

    # 将配置文件中的信息载入至类中
    def __init__(self,config_path = "../MQOperator_conf.json"):
        logging.critical("MQOperator start.")
        logging.critical("Loading config from %s ." % config_path)
        try:
            config_dict = get_conf(config_path)
            logging.critical("Your config information is %s ." % config_dict)
            self.ip_address = config_dict['ip_address']
            self.port = config_dict['port']
            self.queue_name = config_dict['queue_name']
            self.username = config_dict['username']
            self.password = config_dict['password']
        except:
            logging.ERROR("The configration file can not load correctly.Please check %s again." % config_path)
            raise Exception

    # 向ActiveMQ发送消息
    def sendToQueue(self,msg):
        # 初始化欲连接的Queue 指定Ip及Port
        conn = stomp.Connection10([(self.ip_address, int(self.port))])
        conn.start()
        # 连接activeMQ 并将访问队列的用户名和密码输入在这里
        conn.connect(self.username, self.password, wait=True)
        # 发送消息，指定发送的队列名及发送的信息 队列名如果MQ不存在则自行创建
        conn.send(self.queue_name, msg)
        # 断开连接
        conn.disconnect()
        pass

    # 从消息队列接收消息
    def receiveFromQueue(self):
        # 初始化欲连接的Queue 指定Ip及Port
        listener = Listener_k8s()
        conn = stomp.Connection10([(self.ip_address, int(self.port))])
        # 设置Lister的name及数据结构 根据官方文档 Listener应该为一个Class
        conn.set_listener(str(self.queue_name) + "_Listener", listener)
        conn.start()
        conn.connect(self.username, self.password, wait=False)

        # 从指定的队列名字中接收消息
        conn.subscribe(self.queue_name)
        # 此处sleep是为了保证监听成功 实际应用时可以使用循环 持续监听。
        time.sleep(0.5)
        # print "headers : %s" % listener.get_headers()
        # print "message : %s" % listener.get_message()
        conn.disconnect()
        pass



if __name__ == '__main__':

    mqop = MQOperator()
    mqop.sendToQueue('{"name":"Mike"}')
    while True :
        mqop.receiveFromQueue()

    # send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Mike','command':'kubectl get nodes'}")
    # send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Sandy'}")
    # send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Bob'}")
    # receive_from_queue('39.107.239.80', '61613', '/queue/Test_Queue')
    print "end"