# -*- coding: utf-8 -*-
import subprocess
import time
import sched
import datetime
import random
import configparser
import os

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg", encoding='utf-8')
scheduler = sched.scheduler(time.time,time.sleep)
go_hour = config.get("time","go_time")
back_hour = config.get("time","off_time")
directory = config.get("ADB","directory")
screen_dir = config.get("screen","screen_dir")
stagger_min=config.get("time","random_min")
gowork_flow=config.get("operation","gowork_flow")
afterwork_flow=config.get("operation","afterwork_flow")
sleep_time=int(config.get("operation","sleep_time"))
if not os.path.exists(screen_dir):
    os.makedirs(screen_dir)


#转换日期格式作为文件名
now = int(time.time())
timeStruct = time.localtime(now)
strTime = time.strftime("%Y%m%d%H%M%S", timeStruct)
#print(strTime)


# 打开钉钉，关闭钉钉封装为一个妆饰器函数
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        self.screencap()
    return wrapper


class dingding:

    # 初始化，设置adb目录
    def __init__(self,directory):
        self.directory = directory
        # 设备截屏保存到sdcard
        self.adbscreencap = '"%s\\adb" shell screencap -p sdcard/screen%s.png' % (directory,strTime)
        # 传送到计算机
        self.adbpull = '"%s\\adb" pull sdcard/screen%s.png' % (directory,strTime)
        # 删除设备截屏
        self.adbrm_screencap = '"%s\\adb" shell rm -r sdcard/screen%s.png' % (directory,strTime)
        #截屏文件名
        self.filename = 'screen{0}.png'.format(strTime)


    # 截屏>> 发送到电脑 >> 删除手机中保存的截屏
    def screencap(self):
        operation_list = [self.adbscreencap,self.adbpull,self.adbrm_screencap]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("screencap to computer success")

if __name__ == "__main__":
    # ====test
    dingding  = dingding(directory)
    dingding.screencap()
    print('截图在本目录下，文件名:'+dingding.filename)
    # ==== weekend
    # print(is_weekend())
    #import locale
