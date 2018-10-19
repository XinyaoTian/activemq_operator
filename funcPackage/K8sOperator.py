# -*- encoding:utf-8 -*-
from K8sCmdFunc import K8sObject
import os
import re
import logging
logging.basicConfig(level=logging.INFO)

class K8sOperator():

    def __init__(self, k8s_cmd_type, userID, timestamp, image, image_version="lastest", port="[]"):

        self.k8s_obj = K8sObject(k8s_cmd_type, userID, timestamp, image, image_version, port)

    # 建立 Deploy 和 Service
    def setUpDeployAndService(self):
        # os.system(self.k8s_obj.setUpDeployment())
        # os.system(self.k8s_obj.createNodeportService())
        self.k8s_obj.setUpDeployment()
        self.k8s_obj.createNodeportService()

        pass

    # 销毁 Deploy 和 Service
    def tearDownDeployAndService(self):
        # os.system(k8s_obj.closeNodeportService())
        # os.system(tearDownDeployment())
        self.k8s_obj.closeNodeportService()
        self.k8s_obj.tearDownDeployment()

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

    # 利用linux的grep指令 返回deploy相应service的名字
    def findDeployServicePort(self):
        # 组合出的正则匹配式子 其格式为 [0-9]*:[0-9]*
        pattern = "[0-9]*:[0-9]*"
        # 在linux中使用Grep进行 kubectl get service | grep deployname 匹配
        grep_results = os.popen(self.k8s_obj.findPodnameCmd()).readlines()
        ports = []
        for result in grep_results:
            # 将linux命令输出结果与正则式相匹配
            if re.search(pattern, result) is not None:
                port = str(re.search(pattern, result).group(0)).split(":")[1]
                # 立刻返回port
                logging.critical("findDeployServicePort() the port is = %s" % port)
                return port
            else:
                # 否则，继续寻找下一条
                continue
        logging.error("findDeployServicePort() service_name=%s can not find the port." % self.k8s_obj.getDeployName())
        return None



    pass


if __name__ == "__main__":

    # k8s_op = K8sOperator("setUP" , "mike" , '20180202' ,'nginx' , port="[80]")
    # k8s_op.setUpDeployAndService()
    # k8s_op.tearDownDeployAndService()

    output = "jupyter      NodePort    10.104.238.252   <none>        8888:31366/TCP   1d"
    pattern = "[0-9]*:[0-9]*"
    print str(re.search(pattern, output).group(0))

    pass