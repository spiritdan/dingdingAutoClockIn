# -*- coding: utf-8 -*-
import subprocess
import time
import sched
import datetime
import random
import configparser
import os

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg")
scheduler = sched.scheduler(time.time,time.sleep)
go_hour = config.get("time","go_time")
back_hour = config.get("time","off_time")
directory = config.get("ADB","directory")
screen_dir = config.get("screen","screen_dir")
stagger_min=config.get("time","random_min")
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
        #随机数，错开打卡时间，0为没有延迟，参数在dingding.cfg配置random_min
        minute = random_minute(int(stagger_min))
        print("程序启动，休眠{0}秒".format(minute))
        time.sleep(minute)

        print("打开钉钉")
        boolawake=ifawake()
        boollock=ifLock()


        #判断是不是需要唤醒
        if boolawake=='false':
            print('手机处于休眠状态，唤醒手机，解锁手机，运行钉钉')
            operation_list = [self.adbpower, self.adbclear, self.adbopen_dingding]
        elif boollock=='true':
            print("手机处于锁定状态，解锁手机，运行钉钉")
            operation_list = [self.adbclear, self.adbopen_dingding]
        else:
            print("手机处于解锁状态，直接运行钉钉")
            operation_list = [self.adbopen_dingding]

        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键
        time.sleep(20)
        print("open dingding success")
        print("进入打卡界面")
        operation_list1 = [self.adbselect_work, self.adbselect_check_position_card]

        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
            time.sleep(2)
        time.sleep(20)
        print("open playcard success")

        # 包装函数
        func(self, *args, **kwargs)

        print("关闭钉钉")
        operation_list2 = [self.adbkill_dingding, self.adbpower]
        for operation in operation_list2:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding success")
    return wrapper


class dingding:

    # 初始化，设置adb目录
    def __init__(self,directory):
        self.directory = directory
        # 点亮屏幕
        self.adbpower = '"%s\\adb" shell input keyevent 26' % directory
        # 滑屏解锁
        self.adbclear = '"%s\\adb" shell input swipe %s' % (directory,config.get("position","light_position"))
        # 启动钉钉应用
        self.adbopen_dingding = '"%s\\adb" shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1' %directory
        # 关闭钉钉
        self.adbkill_dingding = '"%s\\adb" shell am force-stop com.alibaba.android.rimet'% directory
        # 返回桌面
        self.adbback_index = '"%s\\adb" shell input keyevent 3' % directory
        # 点击工作标签
        self.adbselect_work = '"%s\\adb" shell input tap %s' % (directory,config.get("position","work_position"))
        # 点击考勤打卡标签
        self.adbselect_check_position_card = '"%s\\adb" shell input tap %s' % (directory,config.get("position","check_tap_position"))
        # 点击考勤按钮
        self.adbselect_checkposition = '"%s\\adb" shell input tap %s' % (directory,config.get("position","check_position"))
        # 点击下班打卡按钮
        self.adbclick_playcard = '"%s\\adb" shell input tap %s' % (directory,config.get("position","play_position"))
        # 设备截屏保存到sdcard
        self.adbscreencap = '"%s\\adb" shell screencap -p sdcard/screen%s.png' % (directory,strTime)
        # 传送到计算机
        self.adbpull = '"%s\\adb" pull sdcard/screen%s.png %s' % (directory,strTime,screen_dir)
        # 删除设备截屏
        self.adbrm_screencap = '"%s\\adb" shell rm -r sdcard/screen%s.png' % (directory,strTime)
        #截屏文件名
        self.filename = 'screen{0}.png'.format(strTime)

    # 上班打卡
    @with_open_close_dingding
    def goto_work(self):
        #点击上班按钮
        print('点击上班按钮')
        operation_list = [self.adbselect_checkposition]
        #operation_list = [self.adbselect_check_position_card]

        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)
        self.screencap()
        print("打卡成功")



    # 下班打卡
    @with_open_close_dingding
    def after_work(self):
        #点击下班按钮
        print('点击下班按钮')
        operation_list = [self.adbclick_playcard]
        #operation_list = [self.adbselect_check_position_card]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)

        self.screencap()
        print("afterwork playcard success")


    # 截屏>> 发送到电脑 >> 删除手机中保存的截屏
    def screencap(self):
        operation_list = [self.adbscreencap,self.adbpull,self.adbrm_screencap]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False,stdout=subprocess.PIPE)
            process.wait()
        print("screencap to computer success")

def ifawake():
    adbawake = '"%s\\adb" shell dumpsys window policy|find /I "mAwake"'% directory

    process = subprocess.Popen(adbawake, shell=True, stdout=subprocess.PIPE)
    process.wait()
    for line in process.stdout.readlines():
        ##blow for pycharm and cygwin show chinese#
        output = line.decode('utf-8')
        bool_Awake = output.split('=')[-1].strip()
        #print(output)
    return bool_Awake

def ifLock():
    #True为锁屏 false为已解锁
    adbawake = '"%s\\adb" shell dumpsys window policy|find /I "isStatusBarKeyguard"'% directory

    process = subprocess.Popen(adbawake, shell=True, stdout=subprocess.PIPE)
    process.wait()
    for line in process.stdout.readlines():
        ##blow for pycharm and cygwin show chinese#
        output = line.decode('utf-8')
        bool_lock = output.split('=')[-1].strip()
        #print(bool_lock)
    return bool_lock

# 随机打卡时间段(待完善)
def random_minute(min):
    return random.randint(0,60*min)


if __name__ == "__main__":
    # ====test
    dingding  = dingding(directory)
    dingding.goto_work()
    # ==== weekend
    # print(is_weekend())
    #import locale
