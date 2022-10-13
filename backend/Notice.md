# Notice

## 代码生成器

- project.yaml 的路径问题，关系到里面的 user.dir

- 要加 pom.xml
```xml
<dependency>
    <groupId>io.mybatis</groupId>
    <artifactId>mybatis-mapper</artifactId>
    <version>2.0.0</version>
</dependency>
<dependency>
    <groupId>io.mybatis</groupId>
    <artifactId>mybatis-service</artifactId>
    <version>2.0.0</version>
</dependency>
<dependency>
    <groupId>io.mybatis</groupId>
    <artifactId>mybatis-activerecord</artifactId>
    <version>2.0.0</version>
</dependency>
```

## 启动

- 加 mysql 数据源

- 如果有必要，也可以改服务器端口号

- 测试的时候一定要带上完整路径（/testUsers/1）

- 测试 sql
```sql
drop database if exists test;

create database test;

use test;

drop table if exists test_user;

create table test_user(
    id int auto_increment primary key,
    name varchar(255) not null default 'user',
    password varchar(255) not null default 'QvQ',
    birthday date,
    email varchar(255)
);

insert into test_user(name, password, birthday, email)
values('a','123456','1985-09-11','test_1@test.example');

insert into test_user(name, password, birthday, email)
values('b','7891011','1986-09-11','test_2@test.example');

insert into test_user(name, password, birthday, email)
values('c','simple_password','2000-09-11','test_3@test.example');

insert into test_user(name, password, birthday, email)
values('d','what','2001-09-11','test_4@test.example');

```

## 注意

- controller 中会有 Long（主要是数据库中的 int） 无法映射到 Integer 的问题

- 如果不带路径参数的话，一定要在模板代码中去掉 `@RequestBody` 注解，不然获取不到

## 待办

- 将 model 里面的模板代码改用 lombok