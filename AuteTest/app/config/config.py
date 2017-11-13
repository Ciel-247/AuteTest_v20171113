# -*-coding:utf-8*-
"""
@ Version : 0.1
@ Author  : xzl
@ File    : config.py
@ Project : AutoTest
@ Create Time: 2017-10-25
@ Python version : 3.x

interfaces-test = 1   接口测试 ,1 表示此项目要进行测试 ，0表示此项目不进行测试，
suites-test  多接口测试
perf-test  单元级压力测试
UI-test  UI自动化测试
"""

#有四种种类的自动化测试，需要单独配置，分别是 单接口测试、多接口（接口之间有依赖）测试、轻量级压力测试（并发数小于50）、UI自动化测试


#单接口测试场景配置 INTERFACES_TEST= 1 ，为 1 时表示此场景要进行测试，0为不进行测试，默认为0
INTERFACES_TEST = 0   #单接口测试
SUITES_TEST = 1     #多接口的业务流测试 (后面接口对前面的接口有数据依赖)
PERF_TEST = 0    #单元级性能测试
UI_TEST = 0     #UI自动化测试

CASE_HEADER_PATH = 'app/constructor/template/header.txt'
CASE_CONTENT_PATH = 'app/constructor/template/content.txt'
CREATE_CASE_PATH = 'app/constructor/case/'
INTERFACES_TEST_REPORT_PATH = 'app/report/report_interfaces_test.html'

REPORT_PATH="app/report/report.html"
# xtest report project config

SWITCH = 1
# SWITCH 如果配置为1 则使用bstesterrunner模板  如果为0 则使用其他报告模板
#PROJECT_ID = '5924d39d47fc89719870597c'
#APP_ID = 'c52523ca401711e7bb0900163e006b26'
#APP_KEY = 'c526b58c401711e7bb0900163e006b26'

