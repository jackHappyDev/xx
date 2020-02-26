from flask import Flask,render_template,request,url_for,redirect,make_response,send_file, send_from_directory,jsonify,json
from os import *
from Project import VideoModu
from Project import TimeMakerMethod
from flask_bootstrap import Bootstrap
from Project import Socket_client

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

Bootstrap(app)

#启动测试
@app.route('/')
def hello():

    return render_template('index.html',name='https://upload.jianshu.io/users/upload_avatars/9390216/d054ce9c-0dfc-4c28-9d5a-e8ce047cec77.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96/format/webp')


#关键字搜索
@app.route('/videoSearch/',methods=['POST','GET'])
def kwSearchMethod():
    kw = request.args.get('kw')
    list = VideoModu.getFilterVideoinfoById(kw)
    dt = ResponseMethod(0,'ok',list)
    return jsonify(dt)

#获取首页信息
@app.route('/getFrontpage',methods=['POST','GET'])
def getFrontpage():
    list = VideoModu.getVideoCategoryList()
    dt = ResponseMethod(0, 'ok', list)
    return jsonify(dt)

#开始聊天用于H5调用
@app.route('/startChat')
def startChat():
    Socket_client.client_start()

@app.route('/register',methods=['POST'])
def register():
    # get_data = json.loads(request.get_data(as_text=True))
    username = request.form['name']
    password = request.form['word']
    print(username,password)
    return jsonify({'username':username,'password':password}),201


#定时采集数据到数据库
@app.route('/timeperMethod')
def timeperMethod():

    pass

##############################错误或者服务器错误##################################################################################################
# @app.errorhandler(404)
# def page_not_found(e):
#     if request.url.find('api') != -1:
#         return jsonify({'error': '请求的资源不存在', 'code': '404', 'data': ''})
#     return render_template('error/404.html'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500

def ResponseMethod(code,msg,records):
    data = {
        'code': code,
        'msg': msg,
        'records':records,
    }
    return data
################################################################################################################################


if __name__ == '__main__':

    app.run('0.0.0.0',debug=True,port='9527')
    # TimeMakerMethod.everyTimeRun()