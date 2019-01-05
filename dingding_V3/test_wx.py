from wxpy import *
import time
import schedule
import holiday as holiday, DingDing as Ding
import configparser
import check_holiday
import random
import datetime
config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg", encoding='utf-8')
directory = config.get("ADB","directory")
gowork_time=config.get("time","go_time")
offwork_time=config.get("time","off_time")
stagger_min=config.get("time","random_min")
#target "self_"为微信助手 或者输入用户名发送给其他人。
#target="self_"
target=config.get("weixin","target")
sex=config.get("weixin","sex")
city=config.get("weixin","city")
#print(target,sex,city)


bot = Bot(qr_path="qr.png",cache_path=True)
print('微信启动')
if target=='self_':
    bot_target=bot.file_helper
else:
    if sex=="MALE":
        bot_target = bot.friends().search(target, sex=MALE, city=city)[0]
    if sex=="FEMALE":
        bot_target = bot.friends().search(target, sex=FEMALE, city=city)[0]

#延迟是防止打卡的机子在扫微信时候触发事件
#time.sleep(10)

def job_gowork():
    choliday = checkday()
    holiday_status = choliday['work_status']
    if holiday_status == 0:
        second = random_minute(int(stagger_min))
        str_time=string_toDatetime(gowork_time,second)
        #print("程序启动，休眠{0}秒".format(second))
        msg='今天是：{0}-{1:02d}-{2:02d},{3},将在{4}打卡'.format(choliday['year'],choliday['month'], choliday['day'], choliday['wday'],str_time)
        print(msg)
        bot_target.send(msg)
        time.sleep(second)
        try:
            dingding = Ding.dingding(directory)
            dingding.goto_work()
            png = dingding.filename
            print('D:\\dingding\\' +png)
            bot_target.send('上班打卡')
            bot_target.send_image('D:\\dingding\\' + png)
        except Exception as e:
            print(e)
            bot_target.send('打卡失败:' + e)
            exit()
    else:
        msg='今天是：{0}-{1:02d}-{2:02d},{3},今天不用打卡'.format(choliday['year'],choliday['month'], choliday['day'], choliday['wday'])
        print(msg)
        bot_target.send(msg)


def job_offwork():
    choliday = checkday()
    holiday_status = choliday['work_status']
    if holiday_status == 0:
        second = random_minute(int(stagger_min))
        str_time = string_toDatetime(offwork_time, second)
        # print("程序启动，休眠{0}秒".format(second))
        msg = '今天是：{0}-{1:02d}-{2:02d},{3},将在{4}打卡'.format(choliday['year'],choliday['month'], choliday['day'], choliday['wday'],str_time)
        print(msg)
        print(second)
        bot_target.send(msg)
        time.sleep(second)
        try:
            dingding = Ding.dingding(directory)
            dingding.after_work()
            png = dingding.filename

            print('D:\\dingding\\' +png)
            bot_target.send('下班打卡')
            bot_target.send_image('D:\\dingding\\' + png)
        except Exception as e:
            print(e)
            bot_target.send('打卡失败:' + e)
            exit()
    else:
        msg='今天是：{0}-{1:02d}-{2:02d},{3},今天不用打卡'.format(choliday['year'],choliday['month'], choliday['day'], choliday['wday'])
        print(msg)
        bot_target.send(msg)
def random_minute(min):
    return random.randint(0,60*min)

def string_toDatetime(st,seconds):
    dt= datetime.datetime.strptime(st, "%H:%M")
    #print(dt)
    new_dt=dt+ datetime.timedelta(seconds=int('+{0}'.format(seconds)))
    str_dt=new_dt.strftime("%H:%M")
    print('随机到：',str_dt,'开始')
    return str_dt

def checkday():
    now = int(time.time())
    timeStruct = time.localtime(now)
    year = timeStruct.tm_year
    month = timeStruct.tm_mon
    day = timeStruct.tm_mday

    # 工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
    date = "{0}{1:02d}{2:02d}".format(year, month, day)
    choliday = check_holiday.checkholiday(date)
    choliday['year'] = year
    choliday['month'] = month
    choliday['day'] = day
    print(choliday)
    return choliday

schedule.every().day.at(gowork_time).do(job_gowork)
schedule.every().day.at(offwork_time).do(job_offwork)

while True:
    schedule.run_pending()


embed()