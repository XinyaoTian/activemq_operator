# -*- encoding:utf-8 -*-
import stomp
import time
from datetime import datetime
import logging
logging.basicConfig(level=logging.ERROR)

msg_list = []

# 向消息队列发送消息
def send_to_queue(ip_addr, port, queue_name, msg):
    # 初始化欲连接的Queue 指定Ip及Port
    conn = stomp.Connection10([(ip_addr, int(port))])
    conn.start()
    # 连接activeMQ 并将访问队列的用户名和密码输入在这里
    conn.connect("admin","admin",wait=False)
    # 发送消息，指定发送的队列名及发送的信息 队列名如果MQ不存在则自行创建
    conn.send(queue_name , msg)
    # 断开连接
    conn.disconnect()
    pass

# Listener 类
class Listener(stomp.ConnectionListener):
    def __init__(self):
        # logging.INFO(str(datetime.now()) + ":A new Listener has been created.")
        self.headers = ""
        self.message = ""

    def on_message(self, headers, message):
        # logging.INFO(str(datetime.now()) + 'headers: %s' % headers)
        # logging.INFO(str(datetime.now()) + 'message: %s' % message)
        self.headers = headers
        self.message = message
        print headers
        # print message
        # print type(headers)
        # print type(message)
        print "After eval : %s" % eval(message)
        # Actions after received messages here:
        # ----------- #


        # ----------- #

    def get_headers(self):
        return self.headers

    def get_message(self):
        return self.message

# 从消息队列接收消息
def receive_from_queue(ip_addr, port, queue_name):
    # 初始化欲连接的Queue 指定Ip及Port
    listener = Listener()
    conn = stomp.Connection10([(ip_addr, int(port))])
    # 设置Lister的name及数据结构 根据官方文档 Listener应该为一个Class
    conn.set_listener(str(queue_name) + "_Listener", listener)
    conn.start()
    conn.connect("admin","admin",wait=False)
    # 从指定的队列名字中接收消息
    conn.subscribe(queue_name)
    time.sleep(0.1)
    # print "headers : %s" % listener.get_headers()
    # print "message : %s" % listener.get_message()
    conn.disconnect()
    pass


if __name__ == '__main__':
    send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Mike','command':'kubectl get nodes'}")
    send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Sandy'}")
    send_to_queue('39.107.239.80', '61613', '/queue/Test_Queue', "{'name':'Bob'}")
    receive_from_queue('39.107.239.80', '61613', '/queue/Test_Queue')
    print "end"