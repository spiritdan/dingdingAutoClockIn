from wxpy import *
import dingding.DingDing as Ding
import time
import schedule
import dingding.holiday as holiday
import configparser

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg")
directory = config.get("ADB","directory")
gowork_time=config.get("time","go_time")
offwork_time=config.get("time","off_time")

now = int(time.time())
timeStruct = time.localtime(now)
year = timeStruct.tm_year
month = timeStruct.tm_mon
day = timeStruct.tm_mday
#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
holiday_status=holiday.check_holiday(year,month,day)

bot = Bot(qr_path="qr.png",cache_path=True)
my_friend = bot.friends().search('spirit', sex=MALE, city='苏州')[0]
print('微信启动')
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
            my_friend.send('上班打卡')
            my_friend.send_image('D:\\dingding\\' + png)
        except Exception as e:
            print(e)
            my_friend.send('打卡失败:' + e)
            exit()
    else:
        my_friend.send('今天不干活')


def job_offwork():
    print("开始下班打卡调度")
    if holiday_status == 0:
        try:
            dingding = Ding.dingding(directory)
            dingding.after_work()
            png = dingding.filename

            print('D:\\dingding\\' +png)
            my_friend.send('下班打卡')
            my_friend.send_image('D:\\dingding\\' + png)
        except Exception as e:
            print(e)
            my_friend.send('打卡失败:' + e)
            exit()
    else:
        my_friend.send('今天不干活')

schedule.every().day.at(gowork_time).do(job_gowork)
schedule.every().day.at(offwork_time).do(job_offwork)

while True:
    schedule.run_pending()


embed()