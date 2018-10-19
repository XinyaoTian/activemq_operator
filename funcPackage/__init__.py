# -*- encoding:utf-8 -*-

# {
# 	"type":"setup / teardown / cycle",
# 	"userID":"123456",
# 	"timestamp":"time"
# 	"image":"nginx",
# 	"imageversion":":lastest",
# 	"port":"[80,90,8080]"
# 	"lifespan":"3600"
# }
#
# read os information in linux:
#
# Python 2.7.15 |Anaconda, Inc.| (default, May  1 2018, 23:32:55)
# [GCC 7.2.0] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import os
# >>> os.system("kubectl get pods | grep ju")
# jupyter-68f8fc6dff-ww5c9              1/1       Running   0          1d
# 0
# >>> result = os.system("kubectl get pods | grep ju")
# jupyter-68f8fc6dff-ww5c9              1/1       Running   0          1d
# >>> print result
# 0
# >>> type(result)
# <type 'int'>
# >>> result = os.popen("kubectl get pods | grep ju")
# >>> print result
# <open file 'kubectl get pods | grep ju', mode 'r' at 0x7fded6743660>
# >>> type(result)
# <type 'file'>
# >>> result = os.popen("kubectl get pods | grep ju").readlines
# >>> type(result)
# <type 'builtin_function_or_method'>
# >>> result = os.popen("kubectl get pods | grep ju").readlines()
# >>> type(result)
# <type 'list'>
# >>> len(result)
# 1
# >>> for r in result:
# ... print r
#   File "<stdin>", line 2
#     print r
#         ^
# IndentationError: expected an indented block
# >>> for r in result:
# ...     print r
# ...
# jupyter-68f8fc6dff-ww5c9              1/1       Running   0          1d
#
# >>> for r in result:
# ...     print r
# ...     print type(r)
# ...
# jupyter-68f8fc6dff-ww5c9              1/1       Running   0          1d
#
# <type 'str'>
# >>>