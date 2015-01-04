#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__create__ = '2014/12/27'

import re


class FieldType(object):
    """FiledType类的目标是根据预处理后的field_line，提取出创建mysql table所需要的field type
    对于numeric类型而言，包括类型(numeric)、长度(length)、精度(precision)、是否为无符号(unsigned)、是否填充0(zerofill)
    对于character类型而言，包括类型(character)、长度(length)、字符集(charset)以及校对规则(collate)
    对于datetime类型而言，包括类型(datetime)、精度(fsp)
    对于enum/set类型而言，包括类型(enum_set)以及枚举或集合值(val)
    """
    #字段顺序(m,d,unsigned,zerofill)
    numeric_type_default = {
        'bit': (1, 0, 0, 0),
        'tinyint': (1, 0, 1, 1),
        'bool': (0, 0, 0, 0),
        'boolean': (1, 0, 1, 1),
        'smallint': (1, 0, 1, 1),
        'mediumint': (1, 0, 1, 1),
        'int': (1, 0, 1, 1),
        'integer': (1, 0, 1, 1),
        'bigint': (1, 0, 1, 1),
        'decimal': (1, 1, 1, 1),
        'dec': (1, 1, 1, 1),
        'numerical': (1, 1, 1, 1),
        'fixed': (1, 1, 1, 1),
        'float': (1, 1, 1, 1),    #decided by hardware
        'double': (1, 1, 1, 1),
    }

    def __init__(self, filed_line):
        self.numeric = None
        self.datetime = None
        self.character = None
        self.enum_set = None
        self.field_line = filed_line

    def __unicode__(self):
        self.get_obj()
        return self.get_mysql_str()

    def get_obj(self):
        """解析行，返回Field对象，返回None表明语法不正确
        :return: 返回FieldType对象
        """
        try:
            self.__reg_numeric()
            if not self.numeric:
                self.__reg_character()
                if not self.character:
                    self.__reg_datetime()
                    if not self.datetime:
                        self.__reg_enum_set()
        except Exception, ex:
            print str(ex)
        return None

    def get_mysql_str(self):
        """生成mysql字段字符
        :return: 返回mysql字段字符
        """
        str = ''
        if self.numeric:
            str = self.numeric
            if self.length and self.numeric_type_default.get(self.numeric)[0]:
                str += '(%s' % self.length
                if self.precision and self.numeric_type_default.get(self.numeric)[1]:
                    str += ',%s)' % self.precision
                else:
                    str += ')'
            if self.unsigned:
                str += ' unsigned'
            if self.zerofill:
                str += ' zerofill'
        elif self.datetime:
            str = self.datetime
            if self.fsp is not None:
                str += '(%s)' % self.fsp
        elif self.character:
            str = self.character
            if self.length:
                str += '(%s)' % self.length
            if self.charset:
                str += ' charset %s' % self.charset
            if self.collate:
                str += ' collate %s' % self.collate
        elif self.enum_set:
            str = self.enum_set
            if self.val:
                str += '(%s)' % self.val
        return str

    def __reg_numeric(self):
        """解析numeric
        :return:返回当前fileType对象
        """
        type_pattern = re.compile(r"""
            (?<=\s)
            (?P<numeric>(?:tiny|small|medium|big)?int|bit|bool(?:ean)?|float|double|numeric|fixed|dec(?:imal)?)
            (?:\((?P<length>\d+)(?:,(?P<precision>\d+))?\))?
            (?!\w)
        """, re.X)
        m = type_pattern.search(self.field_line)
        if m:
            reg_result = m.groupdict()
            self.numeric = reg_result.get('numeric', None)
            if self.numeric:
                self.length = reg_result.get('length', None)
                self.precision = reg_result.get('precision', None)
                self.unsigned = ('unsigned' in self.field_line)
                self.zerofill = ('zerofill' in self.field_line)
                return self
        return None

    def __reg_datetime(self):
        """解析datetime
        :return:返回当前fileType对象
        """
        type_pattern = re.compile(r"""
            (?<=\s)
            (?P<datetime>date(?:time)?|timestamp|year)
            (?:\((?P<fsp>\d+)\))?
            (?!\w)
        """, re.X)

        m = type_pattern.search(self.field_line)
        if m:
            reg_result = m.groupdict()
            self.datetime = reg_result.get('datetime', None)
            if self.datetime:
                self.fsp = reg_result.get('fsp', None)
                if self.datetime == 'year' and self.fsp not in ['2', '4']:
                    self.fsp = 4
                elif self.fsp in ['datetime', 'timestamp']:
                    if self.fsp not in range(0, 7):
                        self.fsp = 0
                elif self.fsp == 'date':
                    self.fsp = None
                return self
        return None

    def __reg_character(self):
        """解析character
        :return:返回当前fileType对象
        """
        type_pattern = re.compile(r"""
            (?<=\s)
            (?P<character>(?:var)?char|(?:var)?binary|(?:(?:tiny|medium|long)?(?:text|blob)))
            (\((?P<length>\d+)\))?
            (\s+
            (?:charset|character set)\s+(?P<charset>\w+))?
            (\s+
            collate\s+(?P<collate>\w+))?
            (?!\w)
        """, re.X)
        m = type_pattern.search(self.field_line)
        if m:
            reg_result = m.groupdict()
            self.character = reg_result.get('character', None)
            if self.character:
                self.length = reg_result.get('length', None)
                self.charset = reg_result.get('charset', None)
                self.collate = reg_result.get('collate', None)
                return self
        return None

    def __reg_enum_set(self):
        """解析enum/set
        :param field_line: 经过预处理后的filed描述
        :return:返回当前fileType对象
        """
        type_pattern = re.compile(r"""
            (?<=\s)
            (?P<enum_set>enum|set)
            (?:\((?P<val>.+?)\))?
            (?!\w)
        """, re.X)
        m = type_pattern.search(self.field_line)
        if m:
            reg_result = m.groupdict()
            self.enum_set = reg_result.get('enum_set', None)
            if self.enum_set:
                self.val = reg_result.get('val', None)
                return self
        return None

if __name__ == '__main__':
    s = r"""field `id` enum('1','2') charset utf8 collate latin1_general_cs auto_increment pk"""
    a = FieldType()
    a.get_obj(s)
    #print str(ft)
    print a.get_mysql_str()