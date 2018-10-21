# -*- encoding:utf-8 -*-

import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='./logs/MQreceiver.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', filemode='w',level = logging.ERROR,datefmt='%Y-%m-%d %I:%M:%S %p')

class K8sObject():

    # 需要的类型为 k8s_cmd 的类型 用户标识 启动的镜像 以及时间戳
    def __init__(self , k8s_cmd_type, deploy_name, userID, timestamp, image, image_version="latest", port="[]"):
        self.type = k8s_cmd_type
        self.userID = userID
        self.image = image
        self.image_version = image_version
        self.timestamp = timestamp
        self.port = eval(port)
        # 注意！ 销毁的deployement的时间戳是setUP时的timestamp！
        # self.k8s_deploy_name = "%s-%s-%s" % (str(self.image),
        #                                 str(self.userID),
        #                                 str(self.timestamp))
        self.k8s_deploy_name = deploy_name
        logging.info("New K8sOperator instance has been created.")
        logging.info("Instance_Info: type = %s ; userID = %s ; image = %s ; image_version = %s ; timestamp = %s ; port = %s" %
                     (str(self.type) , str(self.userID) , str(self.image),
                      str(self.image_version), str(self.timestamp), str(self.port))
                     )

    # 创建deployment 的函数 , return string 相应的kubectl命令
    def setUpDeployment(self):
        # 组合成命令为类似 kubectl create deployment nginx-mike-20180502 --image=nginx:lastest 的形式
        k8s_cmd = "kubectl create deployment %s --image=%s:%s" % (self.k8s_deploy_name, str(self.image), str(self.image_version))
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

        # 如果port这个list中的数值为0 即没有要指定开通的端口
        if len(self.port) is 0 :
            # 这条指令是错误的 开启service必须指定至少一个Port 这会在linux里面报错
            k8s_cmd = "kubectl create service nodeport %s --tcp=???:???"

        # 如果指定了容器端口
        else:
            port_str = ""
            for port in self.port:
                # 这两个port是相同的 k8s这么规定的
                port_str += " --tcp=%s:%s" % (port,port)
            # 组合成为类似 kubectl create service nodeport nginx --tcp=80:80 的命令
            k8s_cmd = "kubectl create service nodeport %s %s" % (self.k8s_deploy_name , port_str)

        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于关闭Service
    def closeNodeportService(self):
        # 组合成类似 kubectl delete service nginx 的命令,
        k8s_cmd = "kubectl delete service %s" % self.k8s_deploy_name
        logging.critical("The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于查询 k8s 启动的service的相关端口
    def findServiceCmd(self):
        k8s_cmd = "kubectl get service | grep %s" % self.k8s_deploy_name
        logging.critical("findServiceCmd() The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于查询 k8s 的 Pod name
    def findPodnameCmd(self):
        k8s_cmd = "kubectl get pods | grep %s" % self.k8s_deploy_name
        logging.critical("findPodnameCmd() The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 用于查询 jupyter 启动时logs 中的 token , 需要传入一个pod name
    def findTokenCmd(self,pod_name):
        k8s_cmd = "kubectl logs %s | grep /?token" % pod_name
        logging.critical("findTokenCmd() The k8s command is:%s" % k8s_cmd)

        return k8s_cmd

    # 返回组合出来的deployname
    def getDeployName(self):
        return self.k8s_deploy_name

    pass



if __name__ == "__main__":
    k8s_obj = K8sObject("setup", "jupyter-mike-0902", "mike" , '20180702' ,'jupyter/mini' , port="[8080]")
    k8s_obj.setUpDeployment()
    k8s_obj.createNodeportService()
    k8s_obj.tearDownDeployment()
    k8s_obj.closeNodeportService()
    k8s_obj.findPodnameCmd()
    k8s_obj.findServiceCmd()
    k8s_obj.findTokenCmd("jupyter-68f8fc6dff-ww5c9")