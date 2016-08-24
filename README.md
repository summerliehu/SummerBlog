SummerBlog是基于《Flask Web开发》这本书而构建的一个博客程序，整体框架基本上按照这本书来构建，后期针对博客的特点进行了一些改动，为了实现一些新的功能增加了一些插件，但核心架构变化不大。
我的开发环境是Ubuntu_16.04_64，Python版本为2.7，依赖插件版本见requirements.txt，未在其他系统和环境下进行测试。

run

db.create_all()

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

then

python manage.py shell

>>Role.insert_roles()

to initialize Role table.