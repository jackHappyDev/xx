from flask import Flask,request,url_for,redirect,make_response,send_file, send_from_directory,jsonify,render_template
from os import *
from Project import VideoModu

app = Flask(__name__)

#启动测试
@app.route('/')
def hello():

    return 'Hello world!'


#关键字搜索
@app.route('/videoSearch/',methods=['POST','GET'])
def kwSearchMethod():
    kw = request.args.get('kw')
    list = VideoModu.getFilterVideoinfoById(kw)
    print(80*'*')
    print(list)
    print(80*'*')
    dt = ResponseMethod(1,'ok',list)
    return jsonify(dt)


#定时采集数据到数据库
@app.route('/timeperMethod')
def timeperMethod():

    pass



def ResponseMethod(code,msg,records):
    data = {
        'code': code,
        'msg': msg,
        'records':records,
    }
    return data


if __name__ == '__main__':

    app.run('0.0.0.0',debug=True,port='9527')