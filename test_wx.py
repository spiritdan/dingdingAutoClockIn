from wxpy import *
import time
import schedule
import holiday as holiday, DingDing as Ding
import configparser
import check_holiday

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg")
directory = config.get("ADB","directory")
gowork_time=config.get("time","go_time")
offwork_time=config.get("time","off_time")
#target "self_"为微信助手 或者输入用户名发送给其他人。
#target="self_"
target='spirit'
sex=MALE
city='苏州'
now = int(time.time())
timeStruct = time.localtime(now)
year = timeStruct.tm_year
month = timeStruct.tm_mon
day = timeStruct.tm_mday

#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
date="{0}{1:02d}{2:02d}".format(year,month,day)
choliday=check_holiday.checkholiday(date)
holiday_status=choliday['work_status']
print(choliday)

bot = Bot(qr_path="qr.png",cache_path=True)
print('微信启动')
if target=='self_':
    bot_target=bot.file_helper
else:
    bot_target = bot.friends().search(target, sex=MALE, city='苏州')[0]

bot_target.send('Hello World!')
#延迟是防止打卡的机子在扫微信时候触发事件
time.sleep(10)

def job_gowork():
    print("开始上班打卡调度")

    if holiday_status == 0:
        try:
            dingding = Ding.dingding(directory)
            dingding.goto_work()
            png = dingding.filename
            print('D:\\dingding\\' +png)
            bot_target.send('上班打卡')
            bot_target.send_image('D:\\dingding\\' + png)
            #bot_target.send('上班打卡')
            #bot_target.send_image('D:\\dingding\\' + png)
        except Exception as e:
            print(e)
           #my_friend.send('打卡失败:' + e)
            bot_target.send('打卡失败:' + e)
            exit()
    else:
        bot_target.send('今天不干活')


def job_offwork():
    print("开始下班打卡调度")
    if holiday_status == 0:
        try:
            dingding = Ding.dingding(directory)
            dingding.after_work()
            png = dingding.filename

            print('D:\\dingding\\' +png)
            #bot_target.send('下班打卡')
            #bot_target.send_image('D:\\dingding\\' + png)
            bot_target.send('下班打卡')
            bot_target.send_image('D:\\dingding\\' + png)
        except Exception as e:
            print(e)
            #bot_target.send('打卡失败:' + e)
            bot_target.send('打卡失败:' + e)
            exit()
    else:
        bot_target.send('今天不干活')

def checkday():
    now = int(time.time())
    timeStruct = time.localtime(now)
    year = timeStruct.tm_year
    month = timeStruct.tm_mon
    day = timeStruct.tm_mday

    # 工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
    date = "{0}{1:02d}{2:02d}".format(year, month, day)
    choliday = check_holiday.checkholiday(date)
    print(choliday)
    return choliday




schedule.every().day.at(gowork_time).do(job_gowork)
schedule.every().day.at(offwork_time).do(job_offwork)

while True:
    schedule.run_pending()


embed()