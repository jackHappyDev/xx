from flask import Flask,render_template,request,url_for,redirect,make_response,send_file, send_from_directory,jsonify
from os import *
from Project import VideoModu
from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

#启动测试
@app.route('/')
def hello():

    return render_template('index.html',name='https://rpg.pic-imges.com/pic/upload/vod/2019-12/1576595925.jpg')


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


#定时采集数据到数据库
@app.route('/timeperMethod')
def timeperMethod():

    pass

##############################错误或者服务器错误##################################################################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

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