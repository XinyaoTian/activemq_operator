# -*-encoding:utf-8-*-
import pymongo
import logging
logging.basicConfig(level=logging.ERROR)

class MongoDBOperator():

    def __init__(self,host,port,DBusername,DBpwd,Database='K8sDB',Collection='K8s_Service_Info'):
        # 需要更改为从配置文件里读进来
        # 数据的host和port
        self.client = pymongo.MongoClient(host=host, port=port)
        # 创建连接的数据库
        self.db = self.client[Database]
        # 数据库的用户名和密码 在docker run的时候设置
        self.db.authenticate(DBusername,DBpwd)
        # 数据库的Collection名
        self.collection = self.db[Collection]

    # 插入一个字典
    def insertDict(self,insert_dict):
        if type(insert_dict) is type({"dict":1}):
            self.collection.insert(insert_dict)
            logging.critical("Your information %s has been inserted into %s.%s"
                             % (str(insert_dict), str(self.db), str(self.collection)))
            return True
        else:
            logging.error("Type of %s is not a dict.Can not insert into MongoDB." % str(insert_dict))
            return False

if __name__ == "__main__":
    msg_dict = {'external_port': '32464', 'token': 'c8d344416a4e394c388a61096c2f776c0c90c0cf75343654',
                'image_version': 'latest', 'pod_name': 'jupyter-mike-0904-c7877874f-xk9zl',
                'timestamp': '20180909',
                'image': 'jupyter/minimal-notebook', 'userID': 'mike',
                'deploy_name': 'jupyter-mike-0904', 'container_port': [8080]}

    mdb_op = MongoDBOperator('39.107.239.80',27017,'k8s_user','mypass')
    mdb_op.insertDict(msg_dict)




