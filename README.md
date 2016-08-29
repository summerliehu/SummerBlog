##说明
***
###概览
SummerBlog是基于《Flask Web开发》这本书而构建的一个博客程序.
我的开发环境是Ubuntu_16.04_64，程序还在OS X EI Captain 上测试通过。Python版本为2.7，依赖插件版本见requirements.txt，未在其他系统和环境下进行测试。
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


虚拟环境准备好之后即可开始程序的运行：

```
(venv) $ cd summerblog
# 创建数据库
(venv) $ python manage.py shell
>>> db.create_all()
# 创建角色
>>> Role.insert_roles()
#数据库创建完毕，在本地出现 data-dev.sqlite文件，此时退出python shell即可开始
(venv) $ python manage.py runserver
```

如果你在继续开发的过程中更改了models.py，需要使用以下代码进行数据库迁移：

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
程序运行界面如下所示：
![screenshot](https://raw.githubusercontent.com/summerliehu/SummerBlog/master/screen.png)

BUGS:

1. error occors when trying to delete a tag: StaleDataError: DELETE statement on table 'tags_to_posts' expected to delete 1 row(s); Only 2 were matched.
