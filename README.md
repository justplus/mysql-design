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

TODO
===============
1. 远程连接数据库，进行字段更新
2. 编辑器和实时PDM预览