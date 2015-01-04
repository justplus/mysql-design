#!/usr/bin/env python
# coding=utf-8
from mysqlDesign.fieldType import FieldType

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__create__ = '2014/12/27'

import re


class Field(object):
    def __init__(self, field_line):
        self.field_name = None
        self.field_comment = None
        self.field_autoinc = None
        self.field_nullable = None
        self.field_default = None
        self.fk_table = None
        self.fk_constraint_delete = None
        self.fk_constraint_update = None
        self.field_line = field_line
        self.post_field_line = field_line
        self.get_obj()

    def __unicode__(self):
        self.get_obj()
        return self.get_mysql_str()

    def get_obj(self):
        #先获取comment的内容
        self.__reg_comment()
        self.__reg_default()
        self.__reg_foreignkey()
        self.__reg_primarykey()
        self.__reg_uniquekey()
        self.__reg_name()
        self.__reg_nullable()
        self.__reg_autoinc()

    def get_mysql_str(self):
        str = ''
        if self.field_name:
            str += '`%s`' % self.field_name
        str += ' ' + unicode(FieldType(self.post_field_line))
        if not self.field_nullable:
            str += ' not null'
        if self.field_autoinc:
            str += ' auto_increment'
        if self.field_default:
            str += ' default %s' % self.field_default
        if self.field_comment:
            str += ' comment \'%s\'' % self.field_comment
        return str

    def __reg_comment(self):
        """获取field行中的评论内容
        :return:填充对象的field_comment并返回对象
        """
        comment_pattern = re.compile(r"""
            \s
            comment\s+('|")(?P<comment>.+?)('|")
        """, re.X)
        m = comment_pattern.search(self.field_line)
        if m:
            self.post_field_line = comment_pattern.sub('', self.post_field_line)
            self.__pre_process()
            reg_result = m.groupdict()
            self.field_comment = reg_result.get('comment', None)

    def __reg_default(self):
        default_pattern = re.compile(r"""
            \s
            default\s+(?P<default>('|")?.+?('|")?)
            \s   #遇到'或"则寻找对应的结束符，否则寻找空格或者结束符
        """, re.X)
        m = default_pattern.search(self.post_field_line)
        if m:
            self.post_field_line = default_pattern.sub('', self.post_field_line)
            self.__pre_process()
            reg_result = m.groupdict()
            self.field_default = reg_result.get('default', None)

    def __reg_nullable(self):
        nullable_pattern = re.compile(r"""
            \s
            not\s+null
            \s
        """, re.X)
        m = nullable_pattern.search(self.post_field_line)
        self.field_nullable = False if m else True

    def __reg_autoinc(self):
        autoinc_pattern = re.compile(r"""
            \s
            auto_increment
            \s
        """, re.X)
        m = autoinc_pattern.search(self.post_field_line)
        self.field_autoinc = True if m else False

    def __reg_primarykey(self):
        pk_pattern = re.compile(r"""
            \s
            pk
            \s
        """, re.X)
        m = pk_pattern.search(self.post_field_line)
        self.field_pk = True if m else False

    def __reg_uniquekey(self):
        uk_pattern = re.compile(r"""
            \s
            uk
            \s
        """, re.X)
        m = uk_pattern.search(self.post_field_line)
        self.field_uk = True if m else False

    def __reg_foreignkey(self):
        fk_pattern = re.compile(r"""
            \s
            fk\s+'(?P<fk_table>\w+)\.(?P<fk_field>\w+)'
            \s*
            (?P<update>(?:restrict|cascade|no\s+action|set\s+null))?
            \s*
            (?P<delete>(?:restrict|cascade|no\s+action|set\s+null))?
            \s
        """, re.X)
        m = fk_pattern.search(self.post_field_line)
        if m:
            self.post_field_line = fk_pattern.sub('', self.post_field_line)
            reg_result = m.groupdict()
            self.fk_table = reg_result.get('fk_table', None)
            self.fk_table_field = reg_result.get('fk_field', None)
            self.fk_constraint_update = reg_result.get('update', None)
            self.fk_constraint_delete = reg_result.get('delete', None)

    def __reg_name(self):
        name_pattern = re.compile(r"""
            `
            (?P<name>\w+)
            `
        """, re.X)
        m = name_pattern.search(self.post_field_line)
        if m:
            self.post_field_line = name_pattern.sub('', self.post_field_line)
            self.__pre_process()
            reg_result = m.groupdict()
            self.field_name = reg_result.get('name', None)

    def __pre_process(self):
        if not self.post_field_line.endswith('\r'):
            self.post_field_line += '\r'

if __name__ == '__main__':
    s = u"""field `user_id` bigint not null  comment '用户编号' fk 'user.id' no action cascade default 'sss'\r"""
    f = Field(s)
    print unicode(f)
    print f.fk_table
    print f.fk_table_field
    print f.fk_constraint_update
    print f.fk_constraint_delete
