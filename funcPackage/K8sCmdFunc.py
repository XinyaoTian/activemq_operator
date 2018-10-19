# -*- encoding:utf-8 -*-

import os
import logging
logging.basicConfig(level=logging.INFO)

class K8sOperator():

    # 需要的类型为 k8s_cmd 的类型 用户标识 启动的镜像 以及时间戳
    def __init__(self , k8s_cmd_type , userID , image , timestamp):
        self.type = k8s_cmd_type
        self.userID = userID
        self.image = image
        self.timestamp = timestamp
        # 注意！ 销毁的deployement的时间戳是setUP时的timestamp！
        self.k8s_deploy_name = "%s-%s-%s" % (str(self.image),
                                        str(self.userID),
                                        str(self.timestamp))
        logging.info("New K8sOperator instance has been created.")
        logging.info("Instance_Info: type = %s ; userID = %s ; image = %s ; timestamp = %s " %
                     (str(self.type) , str(self.userID) , str(self.image) , str(self.timestamp))
                     )

    # 创建deployment 的函数 , return string 相应的kubectl命令
    def setUpDeployment(self):
        # 组合成命令为类似 kubectl create deployment nginx-mike-20180502 --image=nginx 的形式
        k8s_cmd = "kubectl create deployment %s --image=%s" % (self.k8s_deploy_name, str(self.image))
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 销毁deploy 的函数, return string 相应的kubectl命令
    # 注意！ 销毁的deployement的时间戳是setUP时的timestamp！
    def tearDownDeployment(self):
        # 组合成类似 kubectl delete deployment nginx-mike-20180502 的命令
        k8s_cmd = "kubectl delete deployment %s" % self.k8s_deploy_name
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于启动Service , 使k8s的pod暴露一个端口供外网使用
    def createNodeportService(self):
        # 组合成类似 kubectl create service nodeport nginx --tcp=80:80 的命令,
        # 此处的 --tcp=80:80 代表docker容器上开放的端口
        # 至于容器具体分配到了哪个实际的端口 根据k8s
        # k8s随机在30000-32767之间进行分配
        k8s_cmd = "kubectl create service nodeport %s --tcp=80:80" % self.k8s_deploy_name
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于关闭Service
    def closeNodeportService(self):
        # 组合成类似 kubectl delete service nginx 的命令,
        k8s_cmd = "kubectl delete service %s" % self.k8s_deploy_name
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于查询 k8s 启动的service的相关端口
    def grepGetService(self,grep_str):
        k8s_cmd = "kubectl get service | grep %s" % grep_str
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于查询 jupyter 启动时logs 中的 token
    def grepGetToken(self,grep_str):
        k8s_cmd = "kubectl logs service | grep %s" % grep_str
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    pass

if __name__ == "__main__":
    k8s_op = K8sOperator("setUP" , "mike" , 'nginx' , '20180202')
    k8s_op.setUpDeployment()
    k8s_op.tearDownDeployment()