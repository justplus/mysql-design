#!/usr/bin/env python
# coding=utf-8
from mysqlDesign.field import Field

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__create__ = '2014/12/27'


class Table(object):
    def __init__(self,):
        self.table_name = None
        self.table_comment = None
        self.field_list = []

    def extract_field(self, table_str):
        self.__reg_field(table_str)

    def __unicode__(self):
        return """CREATE TABLE `%s` (\n%s%s%s%s) ENGINE=InnoDB DEFAULT CHARSET=utf8;
          """ % (self.table_name, self.__get_fields_str(), self.__get_pk_str(),
               self.__get_uk_str(), self.__get_fk_str())

    def get_mysql_str(self):
        return """CREATE TABLE `%s` (\n%s%s%s%s) ENGINE=InnoDB DEFAULT CHARSET=utf8;
          """ % (self.table_name, self.__get_fields_str(), self.__get_pk_str(),
               self.__get_uk_str(), self.__get_fk_str())

    def __reg_field(self, table_str):
        for line in table_str.split('\n'):
            if line.strip().startswith('field'):
                if not line.endswith('\n'):
                    line += '\n'
                field = Field(line)
                self.field_list.append(field)

    def get_pk(self):
        for field in self.field_list:
            if field.field_pk:
                return field

    def __get_fields_str(self):
        return ",\n".join(map(unicode, self.field_list)) + ',\n'

    def __get_pk_str(self):
        for field in self.field_list:
            if field.field_pk:
                return 'primary key (`%s`),\n' % field.field_name
        return ''

    def __get_uk_str(self):
        str = ''
        for field in self.field_list:
            if field.field_uk:
                str += 'unique key `UK_%s_%s` (`%s`),\n' % (self.table_name, field.field_name, field.field_name)
        return str

    def __get_fk_str(self):
        str = ''
        fk_index = 1
        for field in self.field_list:
            if field.fk_table:
                str += 'constraint `%s_ibfk_%s` FOREIGN KEY (`%s`) REFERENCES `%s` (`%s`) ON DELETE %s ON UPDATE %s,\n' \
                       % (self.table_name, fk_index, field.field_name, field.fk_table, field.fk_table_field,
                        'RESTRICT' if not field.fk_constraint_delete else field.fk_constraint_delete,
                        'RESTRICT' if not field.fk_constraint_update else field.fk_constraint_update)
                fk_index += 1
        return str