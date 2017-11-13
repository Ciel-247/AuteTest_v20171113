# -*-coding:utf-8*-
"""
@ Version : 0.1
@ Author  : xuezl
@ File    : __init__.py
@ Project : base_test
@ Create Time: 2017-05-19 16:40
@ Python version : 3.x
"""

from functools import update_wrapper
from ...config.message import CASE_IS_NOT_DEFINE
from ...config.tables import BaseSqlite

class QueryCaseInfo(BaseSqlite):
    """ 通过用户传递的表名 查询case信息"""
    def __init__(self, table):
        """ 初始化， params参数为装饰器接受参数
        table 参数为 sqlite 中数据表的表名
        """
        self.table = self.table_enu.get(table)

    def __call__(self, function):
        """ 接受被挂在装饰器的方法， 并把方法及参数传递给__wrapper__函数"""
        def wrapper(*args, **kwargs):
            """ 用于处理用户查询信息 """
            del args
            query = self.session.query(self.table).filter_by(**kwargs).all()
            result = dict()
            if query:
                if len(query) > 1:
                    for item in query:
                        item.__dict__.pop('_sa_instance_state')
                        data = item.__dict__
                        result[data.get('id')] = data
                    return result
                result['id'] = query[0].id
                result['uri'] = query[0].uri
                result['body'] = query[0].body
                result['class_name'] = query[0].class_name
                result['func_name'] = query[0].func_name
                result['kwassert'] = query[0].kwassert
                result['caseId'] = query[0].caseId
                result['caseDescription'] = query[0].caseDescription
                return result
            return dict(err=CASE_IS_NOT_DEFINE)
        return update_wrapper(wrapper, function)