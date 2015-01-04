mysql-design
===============
一种快捷的mysql设计：

- 快捷的进行mysql PDM设计

- 按照模板导出报表, 包括数据表定义、物理模型图

- 导出sql语句

使用方式
===============
- 简单的语法

### 实体
表  	table
列  	filed
关系 relation


### filed属性
名称 类型 长度 默认值 是否自增 是否为空 注释


### 关键字
table
filed
relation
comment
pk
uk
fk
default
nullable
one-to-one
one-to-many
many-to-one
many-to-many

- 示例

```model
table `user` comment:'用户信息'

field `id` int auto_increment pk comment:'用户id'
field `class_id` bigint nullable fk:class.id default:0 comment:'班级id'

relation `user`->many-to-many<-`class`
```

TODO
===============
1. 远程连接数据库，进行字段更新