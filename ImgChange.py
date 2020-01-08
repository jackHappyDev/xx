from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import QFileInfo
# import imgOption
import tinify
import os
tinify.key = 'b2P3sYrPfzNB3xPkB8TYMBsbYFQlMWwV'
__author__ = '作者:jack\n'
__date__ = '\n开发时间：2019-12-01 11:20:56'

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(400,400)
        self.myButton = QtWidgets.QPushButton(self)
        self.myButton.setGeometry(10,self.height()-40,self.width()-20,40)
        self.myButton.setObjectName("btn")
        self.myButton.setText("选择文件夹开始压缩")
        self.myButton.clicked.connect(self.msg)

        self.myLabel = QtWidgets.QLabel(self)
        self.myLabel.setGeometry(10,10,self.width()-20,60)
        self.myLabel.setText(__author__+getBalance()+__date__)
        self.myLabel.setStyleSheet("background-color:gary;")
        self.myLabel.setAutoFillBackground(True)

        self.stusLab = QtWidgets.QLabel(self)
        self.stusLab.setGeometry(10, 70, self.width() - 20, self.height()-130)
        self.stusLab.setStyleSheet("background-color:green;")
        self.stusLab.setAutoFillBackground(True)



    def msg(self):
        #选择文件夹路径准备压缩
        directory1 = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        if not directory1:
            return
        #压缩文件启动 从服务器上压缩
        cli(directory1)

class CompressImg ():
    def __init__ (self, finder):
        self.png_path = []
        self.finder = finder
    # 获取图片路径
    def get_img_path(self, finder):
        for p in os.listdir(finder):
            temp_path = os.path.join(finder, p)
            if os.path.isdir(temp_path):
                self.get_img_path(temp_path)
            else:
                if os.path.splitext(p)[1] == '.png' or os.path.splitext(p)[1] == '.jpg' or os.path.splitext(p)[1] == '.jpeg':
                    self.png_path.append(os.path.join(finder, p))
    # 循环文件
    def handle_compress (self):
        for file in self.png_path:
            self.compress_file(os.path.abspath(file))
    # 压缩文件
    def compress_file (self, inputFile, width=None):
        print('-----------------compress start-----------------')
        if not os.path.isfile(inputFile):
            print('这不是一个文件，请输入文件的正确路径!')
            return
        else:
            dirname  = os.path.dirname(inputFile)
            basename = os.path.basename(inputFile)
            fileName, fileSuffix = os.path.splitext(basename)
            print('dirname=%s, basename=%s, fileName=%s, fileSuffix=%s' % (dirname, basename, fileName, fileSuffix))
            if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
                dir_list = dirname.split(self.finder)
                if dir_list[1] != '' and dir_list[1][0] == '/':
                    dir = os.path.join(self.finder, 'tiny', dir_list[1][1:])
                else:
                    dir = os.path.join(self.finder, 'tiny', dir_list[1])
                self.mkdir(dir)
                self.compress(inputFile, f'{dir}/{basename}', width)
            else:
                print(f'{fileName}不支持该文件类型压缩!')
        print('-----------------compress end-----------------')
    # 压缩图片
    def compress (self, inputFile, outputFile, img_width):
        source = tinify.from_file(inputFile)
        if img_width is not None:
            resized = source.resize(method='scale', width=img_width)
            resized.to_file(outputFile)
            print(f'{inputFile}压缩成功!')
            # w = MyWindow()
            # w.stusLab.setText(f'{inputFile}压缩成功!')
        else:
            source.to_file(outputFile)
            print(f'{inputFile}压缩成功!')
            # w = MyWindow()
            # w.stusLab.setText(f'{inputFile}压缩成功!')
    # 新建文件夹
    def mkdir (self, path):
        exist = os.path.exists(path)
        if not exist:
            print(f'建了一个名字叫做{path}的文件夹！')
            os.makedirs(path)
            return True
        else:
            print(f'名字叫做{path}的文件夹已经存在了！')
            return False
def cli (path):
    try:
        tinify.validate()
        if tinify.compression_count < 500:
            print(f'本月已压缩图片次数{tinify.compression_count}')
            ci = CompressImg(path)
            ci.get_img_path(path)
            ci.handle_compress()
        else:
            print(f'本月压缩图片次数不足')
    except tinify.Error as e:
        print(f'{e}error')

def getBalance():
    tinify.validate()
    idx = 500-tinify.compression_count
    return f'本月还剩图片压缩{idx}次'

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())





