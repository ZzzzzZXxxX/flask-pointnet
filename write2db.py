# 将off地址写入数据库
import os
import pandas as pd
from sqlalchemy import create_engine
from shutil import copyfile
cur_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(cur_path, "ModelNet40")
# list of all the categories
directories = [d for d in os.listdir(dir_path)
               if os.path.isdir(os.path.join(dir_path, d))]

load_dict = [["train", "ModelNet40/train"], ["test", "ModelNet40/test"]]
lis=[]
for d in load_dict:
    for i in range(len(directories)):
        label_name = directories[i]
        train_path = os.path.join(dir_path, directories[i], d[0])
        save_path = os.path.join(cur_path, d[1])
        for filename in os.listdir(train_path):
            data = {}
            if '.off' in filename:
                s = os.path.join(train_path, filename)
                data['label']=label_name
                data['f_name']=os.path.splitext(filename)[0]
                copyfile(s,'static/files/'+filename)
                data['f_path']='static/files/'+filename
                lis.append(data)
df = pd.DataFrame(lis)
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask'
USERNAME = 'root'
PASSWORD = ''
engine = create_engine("mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE))
# 如果想要自动建表的话把if_exists的值换为replace, 建议自己建表
df.to_sql("files", engine, if_exists='append', index=False)
print('Read from and write to Mysql table successfully!')

