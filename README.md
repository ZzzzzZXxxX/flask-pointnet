# Flask-PointNet
此版本为PointNet的Web实现，能对3D对象(off文件)可视化，以及预测类别。如果只需对[ModelNet40](https://shapenet.cs.stanford.edu/media/modelnet40_ply_hdf5_2048.zip "With a Title")off文件进行训练，预测类别，可参考此项目的[Core](https://shapenet.cs.stanford.edu/media/modelnet40_ply_hdf5_2048.zip "With a Title")版本。
# 快速部署

### 前提条件
- 安装好相关库
- 基于版本
~~~~
Anaconda 2019.10
tensorflow 1.13.1
keras 2.2.4
flask 
pymysql
......
~~~~

### 步骤

- 解压数据

将[ModelNet40](https://shapenet.cs.stanford.edu/media/modelnet40_ply_hdf5_2048.zip "With a Title")解压在项目根目录

- 数据准备(时间比较长)
~~~~
python dataPrep.py
~~~~
- 训练
~~~~
python train_cls.py
~~~~
- 构建数据库(先在mysql中创建一个数据库 flask，根据自己环境，在configs.py中修改参数)
~~~~
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
~~~~
- 将数据写入数据库(根据自己mysql帐号密码等修改)
~~~~
python write2db.py
~~~~

- 启动服务
~~~~
python app.py
~~~~
