#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__create__ = '2014/12/28'

import re


class Relation(object):
    def __init__(self, relation_str):
        self.relation_str = relation_str
        self.pre_table = None
        self.post_table = None
        self.table_relation = None

    def extract_relation(self):
        self.__reg_relation(self.relation_str)

    def __reg_relation(self, relation_str):
        relation_pattern = re.compile(r"""
            relation\s+`(?P<table1>.+?)`-\>(?P<relation>1-1|1-n|n-1|n-n)\<-`(?P<table2>.+?)`
        """, re.X | re.M)
        m = relation_pattern.search(relation_str)
        if m:
            reg_result = m.groupdict()
            self.pre_table = reg_result.get('table1', None)
            self.post_table = reg_result.get('table2', None)
            self.table_relation = reg_result.get('relation', None)

