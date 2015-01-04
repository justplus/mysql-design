#!/usr/bin/env python
# coding=utf-8
import copy
from mysqlDesign.relation import Relation
from mysqlDesign.table import Table

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__create__ = '2014/12/27'

import re


class Database(object):
    def __init__(self, model_str):
        self.model_str = model_str
        self.table_list = []
        self.relation_list = []

    def add_relation(self):
        for line in model_str.split('\n'):
            if line.strip().startswith('relation'):
                if not line.endswith('\n'):
                    line += '\n'
                relation = Relation(line)
                relation.extract_relation()
                if relation.pre_table and relation.post_table and relation.table_relation:
                    self.relation_list.append(relation)

    def add_table(self):
        table_pattern = re.compile(r"""
            table\s+`(?P<tabel_name>\w+)`\s+(?:comment\s+'(?P<table_comment>.+)')?
            (?P<table_content>[\s\S]+?)
            -{3}
        """, re.X | re.M)
        m = table_pattern.findall(self.model_str)
        for table_info in m:
            table = Table()
            table.table_name = table_info[0]
            table.table_comment = table_info[1]
            table.extract_field(table_info[2])
            self.table_list.append(table)

    def add_relation_table(self):
        for relation in self.relation_list:
            pre_table_name = relation.pre_table
            post_table_name = relation.post_table
            table_relation = relation.table_relation
            post_table = self.__find_table(post_table_name)
            pre_table = self.__find_table(pre_table_name)
            if table_relation == '1-n':
                if post_table and pre_table:
                    fk_field = copy.deepcopy(pre_table.get_pk())
                    #对字段做些更改
                    fk_field.field_autoinc = False
                    fk_field.field_pk = False
                    fk_field.fk_table = pre_table_name
                    fk_field.fk_table_field = fk_field.field_name
                    fk_field.field_name = '%s_%s' % (pre_table_name, fk_field.field_name)
                    post_table.field_list.append(fk_field)
            elif table_relation == 'n-1':
                if post_table and pre_table:
                    fk_field = copy.deepcopy(post_table.get_pk())
                    #对字段做些更改
                    fk_field.field_autoinc = False
                    fk_field.field_pk = False
                    fk_field.fk_table = post_table_name
                    fk_field.fk_table_field = fk_field.field_name
                    fk_field.field_name = '%s_%s' % (post_table_name, fk_field.field_name)
                    pre_table.field_list.append(fk_field)
            elif table_relation == 'n-n':
                pre_table_pk_copy = copy.deepcopy(pre_table.get_pk())
                post_table_pk_copy = copy.deepcopy(post_table.get_pk())
                pre_table_pk_copy.field_autoinc = False
                pre_table_pk_copy.field_pk = False
                pre_table_pk_copy.field_name = '%s_%s' % (pre_table_name, pre_table_pk_copy.field_name)
                post_table_pk_copy.field_autoinc = False
                post_table_pk_copy.field_pk = False
                post_table_pk_copy.field_name = '%s_%s' % (post_table_name, post_table_pk_copy.field_name)
                table_str = u"""field `%s_%s` %s fk '%s.%s'\nfield `%s_%s` %s fk '%s.%s'\n""" % (
                    pre_table.table_name, pre_table.get_pk().field_name, pre_table_pk_copy.get_mysql_str(),
                    pre_table_name, pre_table.get_pk().field_name,
                    post_table.table_name, post_table.get_pk().field_name, post_table_pk_copy.get_mysql_str(),
                    post_table_name, post_table.get_pk().field_name
                )
                relation_table = Table()
                relation_table.extract_field(table_str)
                relation_table.table_name = '%s_%s' % (pre_table.table_name, post_table.table_name)
                relation_table.table_comment = u'%s-%s关联表' % (pre_table.table_name, post_table.table_name)
                #relation_table.field_list = [pre_table_pk_copy, post_table_pk_copy]
                self.table_list.append(relation_table)

    def __find_table(self, table_name):
        for table in self.table_list:
            if table.table_name == table_name:
                return table
        return None

if __name__ == '__main__':
    model_str = u"""
        ```model
        table `user` comment '用户信息'

        field `id` bigint auto_increment pk comment '用户id'
        field `login_name` varchar(20) not null uk comment '登录名'
        field `user_name` varchar(20) not null comment '用户姓名'
        field `age` tinyint not null default 0 comment '性别'

        ---

        table `class` comment '班级信息'

        field `id` bigint auto_increment pk comment '班级id'
        field `class_name` varchar(50) not null comment '班级名称'

        ---

        table `address` comment '住址'
        field `id` bigint pk not null comment '住址id'
        field `address` varchar(255) not null comment '住址'

        ---

        relation `user`->n-n<-`class`

        relation `user`->1-n<-`address`
        ```
    """
    d = Database(model_str)
    d.add_table()
    d.add_relation()
    d.add_relation_table()
    for table in d.table_list:
        print table.get_mysql_str()

