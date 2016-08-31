##说明
***
###概览
SummerBlog是基于《Flask Web开发》这本书而构建的一个博客程序.
我的开发环境是Ubuntu_16.04_64，程序还在OS X EI Captain 上测试通过。Python版本为2.7，依赖插件版本见requirements.txt，未在其他系统和环境下进行测试。

###功能

目前具有以下功能：

* 添加删除文章
* 添加删除分类（一篇文章只能有一个分类）
* 添加删除标签（每篇文章可以有多个标签）

###使用方法
推荐在虚拟环境下运行。

首先，将程序克隆至本地，然后进入Summerblog文件夹：

```
#建立虚拟环境：
$ cd SummerBlog
$ virtualenv venv
#进入虚拟环境：
$ source venv/bin/activate
#安装依赖：
(venv)$ pip install -r requirements.txt
```
编辑config.py进行配置。

虚拟环境准备好之后需要创建数据库及角色：

```
(venv) $ cd summerblog
# 创建数据库
(venv) $ python manage.py shell
>>> db.create_all()
# 创建角色
>>> Role.insert_roles()
#数据库创建完毕，在本地出现 data-dev.sqlite文件，此时退出python shell即可开始服务器的运行
(venv) $ python manage.py runserver
```
未登录的用户无法看到登录和注册的入口，管理员注册需要使用config.py文件中定义的管理员邮箱进行注册。使用默认配置的开发者可以使用以下测试邮箱注册账号：
邮箱：test_flask2@sina.com
密码:testflask
(请勿更改邮箱密码，方便其他开发者进行登录)
注册入口为：".../register"，登录入口为".../login"。

如果你在继续开发的过程中更改了models.py，需要使用以下代码进行数据库迁移：

```
python manage.py db init #init只需要在首次进行迁移时运行，之后的数据迁移只需要进行migrate和upgrade
python manage.py db migrate
python manage.py db upgrade
```
程序运行界面如下所示：
![screenshot](https://raw.githubusercontent.com/summerliehu/SummerBlog/master/shot.png)

