# 建表写在models.py文件里面
from exts import db

"""
以下表关系：
一个用户对应多篇文章（一对多）
一篇文章对应多个标签，一个标签对应多个文章（多对多）
"""
"""
一对一关系中，需要设置relationship中的uselist=Flase，其他数据库操作一样。
一对多关系中，外键设置在多的一方中，关系（relationship）可设置在任意一方。
多对多关系中，需建立关系表，设置 secondary=关系表
"""

# 用户表
class Files(db.Model):
    label = db.Column(db.String(20))
    f_name = db.Column(db.String(30),primary_key=True)
    f_path = db.Column(db.String(100))