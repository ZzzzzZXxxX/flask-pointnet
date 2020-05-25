import os
from test import Test
from flask import Flask, request, redirect, render_template, url_for, current_app
import configs
from exts import db
import exts
import show
from models import *
from datetime import timedelta
app = Flask(__name__)
# 加载配置文件
app.config.from_object(configs)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=15) #将缓存时间设置为15秒，默认12小时

# db绑定app
db.init_app(app)
# 预测模型
model=Test()
@app.route('/')
def hello_world():
    return redirect(url_for('upload'))
# 负责检索文件图象输出
@app.route('/show/<path>')
def shows(path):
    try:
        show.show_plt('static/files/'+path+'.off')
        return render_template('show.html')
    except:
        return "文件存在问题，构建失败"
#表格分页
@app.route("/list/<int:page>", methods=['GET', 'POST'])
def list(page=1):
    # per_page 为list分页显示的条数
    lis = Files.query.filter_by(label=exts.p_label).paginate(page=page, per_page=10)
    return render_template('list.html', infos=lis.items, pagination=lis)
#上传
@app.route('/upload', methods=['POST', 'GET'])
def upload():

    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'test','test.off')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        try:
            exts.p_label=model.Predict()
            # return redirect(url_for('upload'))\
            return render_template('upload.html',name=exts.p_label,path='static/test.png',style='')
        except:
            return '采样失败！文件可能无法采样'


    return render_template('upload.html',style='style=display:none')


if __name__ == '__main__':
    app.run()
