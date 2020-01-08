#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
    tinypng [-d] <dir>

Options:
    -h,--help   显示帮助菜单
    -d          压缩目录

Example:
    tinypng -d /Users/sunny/Desktop/xxx
"""

import os.path
import tinify, os
from docopt import docopt

__author__ = 'sunny'
__date__ = '2018/09/26'

# 请替换为自己申请的Key
tinify.key = 'b2P3sYrPfzNB3xPkB8TYMBsbYFQlMWwV'

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
        else:
            source.to_file(outputFile)
            print(f'{inputFile}压缩成功!')
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
    tinify.validate()
    print(f'本月已压缩图片次数{tinify.compression_count}')
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

# if __name__ == '__main__':
#     cli()