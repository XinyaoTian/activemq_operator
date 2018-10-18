# -*- encoding:utf-8 -*-
import stomp
import time
from datetime import datetime
import logging
logging.basicConfig(level=logging.ERROR)

from json_reader import get_conf

# msg_list = []

# Listener 类
class Listener(stomp.ConnectionListener):

    # 一个消息需要两个部分: headers 和 message
    def __init__(self):
        self.headers = ""
        self.message = ""

    # 从ActiveMQ中接收到消息时的动作 这个函数是stomp包 fork一个子进程去执行的 因此可以并发
    def on_message(self, headers, message):
        # logging.INFO(str(datetime.now()) + 'headers: %s' % headers)
        # logging.INFO(str(datetime.now()) + 'message: %s' % message)
        self.headers = headers
        self.message = message
        print "headers : %s " % headers
        print "message : %s " % message
        # print type(headers)
        # print type(message)
        print "After eval ,type : %s ; msg : %s" % ( type(eval(message)) , eval(message) )
        # Actions after received messages here:
        # ----------- #


        # ----------- #

    def get_headers(self):
        return self.headers

    def get_message(self):
        return self.message


class MQOperator():

    # 将配置文件中的信息载入至类中
    def __init__(self):
        config_dict = get_conf()
        try:
            self.ip_address = config_dict['ip_address']
            self.port = config_dict['port']
            self.queue_name = config_dict['queue_name']
            self.username = config_dict['username']
            self.password = config_dict['password']
        except:
            logging.ERROR("The configration file can not load correctly.Please check MQOperator_conf.json again.")
            logging.ERROR("Your config info is : %s" % str(config_dict))
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
        listener = Listener()
        conn = stomp.Connection10([(self.ip_address, int(self.port))])
        # 设置Lister的name及数据结构 根据官方文档 Listener应该为一个Class
        conn.set_listener(str(self.queue_name) + "_Listener", listener)
        conn.start()
        conn.connect(self.username, self.password, wait=False)
        # 从指定的队列名字中接收消息
        conn.subscribe(self.queue_name)
        time.sleep(0.1)
        # print "headers : %s" % listener.get_headers()
        # print "message : %s" % listener.get_message()
        conn.disconnect()
        pass



if __name__ == '__main__':

    mqop = MQOperator()
    mqop.sendToQueue('{"name":"Mike"}')
    print mqop.receiveFromQueue()

    # send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Mike','command':'kubectl get nodes'}")
    # send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Sandy'}")
    # send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Bob'}")
    # receive_from_queue('39.107.239.80', '61613', '/queue/Test_Queue')
    print "end"