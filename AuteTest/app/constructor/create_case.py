# -*- coding: utf-8 -*-
"""
@ Version : 0.1
@ Author  : xuezl
@ File    : create_case.py
@ Project : base_test
@ Create Time: 2017-05-25 17:26
"""
from os import listdir ,remove
from ..config import config
from ..config import message
from .use_case_operation import UseCaseOperation
import openpyxl
import logging

class FileMeta:
    """read file headers and content.txt"""
    old_cases = listdir(config.CREATE_CASE_PATH)
    #先将旧的用例文件删除
    [remove(config.CREATE_CASE_PATH + item) for item in old_cases if item not in [
        '__init__.py', '__pycache__']]
    headers = open(config.CASE_HEADER_PATH, 'rb')
    content = open(config.CASE_CONTENT_PATH, 'rb')

    @classmethod
    def __close__(cls):
        """ close all files """
        cls.headers.close()
        cls.content.close()

class CreateCase:
    """自动化测试用例生成"""


    @classmethod
    def import_files_case_to_sqlite(cls):
        """将case_file文件中的全部数据导入sqlite,防备后面组件调用测试用例的元素"""
        work_book = openpyxl.load_workbook("case_file/test-case.xlsx") #读取工作簿，此处工作簿名称写死，可以改成可配置或读取批量的；
        ws = work_book.get_sheet_by_name("interfaces-test") #读取工作表,此处工作表名称写死，可以改成遍历；

        #第一行为表头，不读取，从第二行开始，遍历每行
        for rx in ws.iter_rows(min_row=2):
            params_dict = dict(
                caseId=rx[0].value,
                class_name=rx[1].value,
                func_name=rx[2].value,
                caseDescription=rx[3].value,
                uri=rx[4].value,
                body=rx[5].value,
                kwassert=rx[6].value,
                ifexecute=rx[7].value
            )
            query_info = UseCaseOperation.query_test_case_info(##[lesq??]这里的目的是想要供后续判断这条用例是否已经存在？但是query_test_case_info方法还没有完善？
                uri=params_dict.get('uri'),
                func_name=params_dict.get('func_name'),
                type=0##【lesq??】这里type的作用是什么？？
            )

            if query_info.get('uri') == params_dict.get('uri') and query_info.get('func_name') ==params_dict.get('func_name'):
                return message.CASE_ALREADY_EXISTS##【lesq??】为什么uri和func_name相同的时候就判定CASE_ALREADY_EXISTS???【后面这里要优化一下，加上CaseID来判断重复】
            UseCaseOperation.add_test_case(**params_dict)

    @classmethod
    def get_case_class_name(cls):##[lesq]用于生成用例文件时用作类名
        """获取所有class case name"""
        cls.import_files_case_to_sqlite()
        all_case_info=UseCaseOperation.query_test_case_info(type=0)
        #logging.info(all_case_info)
        class_enu=set()
        for key,value in all_case_info.items():##[lesq]
            if value.get('class_name'):
                class_enu.add(value.get('class_name'))

        return class_enu


    @classmethod
    def get_case_function_name(cls):##[lesq]用于生成用例文件时用作test_case的名字
        """获取同一模块（class）下的所有function name"""
        result= {}
        #logging.info(cls.get_case_class_name())
        for index,class_name in enumerate(cls.get_case_class_name()):
            case_info=UseCaseOperation.query_test_case_info(class_name=class_name, type=0)
            logging.info(case_info)
            if not isinstance(list(case_info.keys())[0], int):
                result.update({class_name: case_info.get('func_name')})
            else:
                case_name = [value.get('func_name') for key, value in case_info.items()]
                result.update({class_name: case_name})

        return result


    @classmethod
    def create_unittest_files(cls):
        """通过 get_case_function_name 函数传递回来的 class_name 和 func_name 批量生成测试文件用例"""
        headers = FileMeta.headers.read().decode()
        content = FileMeta.content.read().decode()

        result = {}
        # logging.info(cls.get_case_class_name())
        for index, class_name in enumerate(cls.get_case_class_name()):
            case_info = UseCaseOperation.query_test_case_info(class_name=class_name, type=0)
            #logging.info(case_info)
            if not isinstance(list(case_info.keys())[0], int):  #单接口用例
                with open(
                    config.CREATE_CASE_PATH + 'test_' + case_info.get('class_name') + '.py', 'a',
                    encoding='utf-8'
                )as file:
                    payload=case_info.get('body')

                    file.write(headers.format(case_info.get('func_name'), case_info.get('func_name')))
                    file.write(content.format('test_' + case_info.get('func_name'), case_info.get('func_name'),case_info.get('caseDescription'),payload.replace(chr(34),"'"),case_info.get('uri'),case_info.get('kwassert'),ifexecute = case_info.get('ifexecute')))
            else: #多接口用例
                with open(
                    config.CREATE_CASE_PATH + 'test_' + class_name.lower() + '.py', 'a',
                    encoding='utf-8'
                )as file:
                    file.write(headers.format(class_name.lower(), class_name))
                    for item in list(case_info.values()):
                        #logging.info(item)
                        payload = item.get('body')
                        file.write(content.format('test_' + item.get('func_name'), item.get('func_name'),
                                                  item.get('caseDescription'), payload.replace(chr(34),"'"),
                                                  item.get('uri'),item.get('kwassert'),ifexecute = item.get('ifexecute')))
                        # logging.info(headers.format(key,key))
                #case_name = [value.get('func_name') for key, value in case_info.items()]
                #result.update({class_name: case_name})

        '''
        for key,value in cls.get_case_function_name().items():
            #logging.info(cls.get_case_function_name().items())
            if not isinstance(value,list):
                with open(
                    config.CREATE_CASE_PATH + 'test_'+ key.lower()+'.py','a',encoding='utf-8'
                )as file:
                    #file.write(headers.format(key, key))
                    #file.write(content.format('test_' + value, value))
                    logging.info("11")
            else:
                with open(
                    config.CREATE_CASE_PATH + 'test_'+ key.lower()+'.py','a',encoding='utf-8'
                )as file:
                    #file.write(headers.format(key, key))
                    for item in value:
                        logging.info("22")
                        #file.write(content.format('test_' + item, item))
                    #logging.info(headers.format(key,key))

        #logger2.error("OK,header")
        #logging.info("case headers\r\n"+headers)
        '''
        #FileMeta.__close__()
        return dict(msg=message.CASE_CREATE_OVER,final_case_path=config.CREATE_CASE_PATH)


