# -*- coding: utf-8 -*-
"""
@ Version : 0.1
@ Author  : xzl
@ File    : create_case.py
@ Project : base_test
@ Create Time: 2017-10-25 17:26
"""

from ..controller import util

class UseCaseOperation:
    """测试控制组件及其操作"""

    @classmethod
    @util.QueryCaseInfo("test_case")
    def query_test_case_info(cls,**kwargs):##[lesq??]这个方法的主要作用是什么？
        """查询指定case 的全部信息"""

    @classmethod
    @util.AddCaseWrapper("test_case")
    def add_test_case(cls, caseId=None, class_name=None, func_name=None,caseDescription=None,uri=None, body=None,kwassert=None):
        """根据表字段增加 test constructor"""

    @classmethod
    @util.ClearTestCase("test_case")
    def clear_test_data(cls):
        """清除sqlite中已跑完的 case 数据"""
