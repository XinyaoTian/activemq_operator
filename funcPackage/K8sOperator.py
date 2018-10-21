# -*- encoding:utf-8 -*-
from K8sCmdFunc import K8sObject
import os
import re
import time
import logging
logging.basicConfig(filename='./logs/MQreceiver.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', filemode='w',level = logging.ERROR,datefmt='%Y-%m-%d %I:%M:%S %p')


class K8sOperator():

    def __init__(self, k8s_cmd_type, deploy_name, userID, timestamp, image, image_version="latest", port="[]"):

        self.k8s_obj = K8sObject(k8s_cmd_type, deploy_name, userID, timestamp, image, image_version, port)

    # 建立 Deploy 和 Service
    def setUpDeployAndService(self):
        os.system(self.k8s_obj.setUpDeployment())
        os.system(self.k8s_obj.createNodeportService())
        # self.k8s_obj.setUpDeployment()
        # self.k8s_obj.createNodeportService()

        pass

    # 销毁 Deploy 和 Service
    def tearDownDeployAndService(self):
        os.system(self.k8s_obj.closeNodeportService())
        os.system(self.k8s_obj.tearDownDeployment())
        # self.k8s_obj.closeNodeportService()
        # self.k8s_obj.tearDownDeployment()

        pass

    # 判定执行何种操作的函数
    # 本函数可以用于执行正确格式下的所有kubectl命令
    # 接下来的各种行为动作也应该在此执行
    def checkAndDoCommandType(self):
        # 若命令类型为setup
        if self.k8s_obj.type is "setup" :
            self.setUpDeployAndService()
            logging.critical("Create k8s deployment %s and service %s." %
                             (self.k8s_obj.getDeployName(),self.k8s_obj.getDeployName()))

        # 若命令类型为teardown
        elif self.k8s_obj.type is "teardown" :
            self.tearDownDeployAndService()
            logging.critical("Delete k8s deployment %s and service %s." %
                         (self.k8s_obj.getDeployName(), self.k8s_obj.getDeployName()))
        else:
            logging.critical("The command type not correct.'type' only 'setup' and 'teardown' can be treated."
                             " Your type = %s ." % self.k8s_obj.type)

    # 专门用于操作k8s集群创建Jupyter的相应函数
    def dealWithJupyter(self):
        # 若命令为setup
        if self.k8s_obj.type is "setup" :
            self.setUpDeployAndService()
            logging.critical("Create k8s deployment %s and service %s." %
                             (self.k8s_obj.getDeployName(),self.k8s_obj.getDeployName()))
            # 等待创建3秒
            time.sleep(3)
            # 利用linux命令寻找pod_name
            pod_name = self.findPodName()
            # 寻找分配好的相应port
            port = self.findDeployServicePort()
            i = 0
            token = self.findLogsToken()
            # 以防日志创建较为缓慢，因此在此循环，等待日志输出
            while i < 5:
                if self.findLogsToken() is not "":
                    token = self.findLogsToken()
                    break
                else:
                    time.sleep(2)
                    i += 0
                    logging.info("Finding logs and token from Pod %s .Times of trying= %s" % (pod_name , str(i)))

            # 如果没找到token ,则返回None 结束该函数
            if token is "" :
                logging.error("Can not find logs and token of Pod %s" % pod_name)
                return None

            # 如果找到了齐全的pod_name port 和token
            logging.critical("Find pod_name=%s port=%s and token=%s" % (pod_name,port,token))
            # ToDo:接下进行数据库操作，将它们写入数据库
            print pod_name
            print port
            print token

            pass

        # 若命令类型为teardown
        elif self.k8s_obj.type is "teardown" :
            self.tearDownDeployAndService()
            logging.critical("Delete k8s deployment %s and service %s." %
                         (self.k8s_obj.getDeployName(), self.k8s_obj.getDeployName()))
        # 否则 类型不为 setup 和 teardown 则报错 什么都不执行
        else:
            logging.critical("The command type not correct.'type' only 'setup' and 'teardown' can be treated."
                             " Your type = %s ." % self.k8s_obj.type)
            return None


        pass


    # 利用linux的grep指令 返回pod 的名字
    def findPodName(self):
        # 组合出的正则匹配式子 其格式为 Deployname[a-z0-9\-]*
        pattern = self.k8s_obj.getDeployName() + "[a-z0-9\-]*"
        # 在linux中使用Grep进行 kubectl get pods | grep deployname 匹配
        grep_results = os.popen(self.k8s_obj.findPodnameCmd()).readlines()
        pod_names = []
        for result in grep_results:
            # 将linux命令输出结果与正则式相匹配
            if re.search(pattern, result) is not None:
                pod_name = re.search(pattern, result).group(0)
                pod_names.append(pod_name)

        # 若找到相应pod
        logging.critical("findPodName() the node_names are/is = %s" % str(pod_names))
        if len(pod_names) == 1:
            logging.critical("findPodName() the node_name is = %s" % str(pod_names[0]))
            return pod_names[0]
        # 若找到多个
        elif len(pod_names) > 1:
            logging.error("Several pod names when K8sOperator.findPodName() finding pod_name = %s."
                          % self.k8s_obj.getDeployName())
            return ""
        # 若没有找到
        else:
            logging.error("No pod whose name includes %s when K8sOperator.findPodName() finding pod_name."
                          % self.k8s_obj.getDeployName())
            return ""

    # 在kubectl的logs中寻找token
    def findLogsToken(self):
        # 获取findPodName()的Pod 名
        pod_name = self.findPodName()
        # 正则表达式
        pattern = "token=[a-f0-9]*"
        outputs_list = os.popen(self.k8s_obj.findTokenCmd(pod_name)).readlines()
        token = ""
        for output in outputs_list:
            # 如果找到token
            if re.search(pattern,output) is not None:
                # 防止切完之后list越界
                if len(str(re.search(pattern,output).group(0)).split("token=")) is 2:
                    token = str(re.search(pattern,output).group(0)).split("token=")[1]
                    logging.critical("findLogsToken() the token is = %s" % token)
                    # 立刻结束函数 因为日志有太多行了
                    return token
            # 否则
            else:
                # 继续找下一条日志
                continue
            # 如果整个日志中都没有token
            logging.error("findLogsToken() can not find the token.Will return None.")
            # 返回None
            return ""

    # //ToDO: 目前仅能返回一个port 。在后续迭代中，如需返回多个port 需要修改这里的函数。
    # 利用linux的grep指令 返回deploy相应service的名字
    def findDeployServicePort(self):
        # 组合出的正则匹配式子 其格式为 [0-9]*:[0-9]*
        pattern = "[0-9]*:[0-9]*"
        # 在linux中使用Grep进行 kubectl get service | grep deployname 匹配
        grep_results = os.popen(self.k8s_obj.findServiceCmd()).readlines()
        # ports = []
        for result in grep_results:
            print result
            # 将linux命令输出结果与正则式相匹配
            if re.search(pattern, result) is not None:
                port = str(re.search(pattern, result).group(0)).split(":")[1]
                # 立刻返回port
                logging.critical("findDeployServicePort() the port is = %s" % str(port))
                return str(port)
            else:
                # 否则，继续寻找下一条
                continue
        logging.error("findDeployServicePort() service_name=%s can not find the port." % self.k8s_obj.getDeployName())
        return ""



    pass


if __name__ == "__main__":

    # k8s_op = K8sOperator("setUP" , "mike" , '20180202' ,'nginx' , port="[80]")
    # k8s_op.setUpDeployAndService()
    # k8s_op.tearDownDeployAndService()

    output = "jupyter      NodePort    10.104.238.252   <none>        8888:31366/TCP   1d"
    pattern = "[0-9]*:[0-9]*"
    print str(re.search(pattern, output).group(0)).split(":")[1]

    pass