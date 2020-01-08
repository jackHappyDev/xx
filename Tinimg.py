from tkinter import *
import tkinter as tk
from tkinter.filedialog import askdirectory
import tinify
import os

tinify.key = 'b2P3sYrPfzNB3xPkB8TYMBsbYFQlMWwV'

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    print(size)
    root.geometry(size)



class Application(tk.Frame):


    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.file_path = ""
        self.create_widgets()


    def create_widgets(self):
        self.AuthorLab = tk.Label(self)
        xx = self.getBalance()
        self.AuthorLab["text"] = "作者:jack\n开发时间：2019-12-01 11:20:56 \n %s" % xx
        self.AuthorLab.pack(side ="top")

        self.ContentLab = tk.Label(self)
        self.ContentLab["text"] = ""
        self.ContentLab.pack(side = "top")
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "    选择要压缩的文件路径   "
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        # self.begincompress = tk.Button(self)
        # self.begincompress["text"] = "    开始压缩   "
        # self.begincompress["command"] = self.compressAction
        # self.begincompress.pack(side="top")

        self.quit = tk.Button(self, text=" 退出  ", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        # self.ContentLab["text"] = getBalance()
        self.file_path = askdirectory()
        # 获取当前目录
        currentDir = self.file_path
        # 压缩的图片类型
        supportImgType = ['.jpg', '.png'];
        self.hi_there["text"] = "    正在压缩中...   "
        # 遍历目录下的图片，并批量压缩图片
        for item in os.listdir(currentDir):
            if item.endswith('.png'):
                xxpath = currentDir+'/' +item
                xxNewpath = currentDir + '/xin_' + item
                print(item)
                if os.path.isfile(xxpath):
                    print('doing:' + xxpath)  # 打印出当前正在压缩的图片名称
                    source = tinify.from_file(xxpath)
                    source.to_file(xxNewpath)
                    print('done:' + item)  # 打印出压缩完成的图片名称


    def compressAction(self):
        self.ContentLab["text"] = "您选择的文件路径问%s" % self.file_path

    def getBalance(self):
        tinify.validate()
        idx = 500 - tinify.compression_count
        return f'本月还剩图片压缩{idx}次'

root = tk.Tk()
center_window(root, 600, 200)
root.maxsize(600, 200)
root.minsize(300, 200)
app = Application(master=root)
app.mainloop()