# -*- coding: utf-8 -*-
"""
@ Version : 0.1
@ Author  : xuezl
@ File    : tables.py
@ Project : base_test
@ Create Time: 2017-05-19 16:09
"""
from .connect import TestCase
from . import SESSION


class BaseSqlite:##【lesq??】这个元类的作用是什么？？？
    """ sqlite 元类"""
    table_enu = {
        'test_case': TestCase
    }
    session = SESSION