import time
import schedule
import holiday as holiday, DingDing as Ding
import configparser
import check_holiday
import random
import datetime

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg",encoding='utf-8')
directory = config.get("ADB","directory")
gowork_time=config.get("time","go_time")
offwork_time=config.get("time","off_time")
stagger_min=config.get("time","random_min")

now = int(time.time())
timeStruct = time.localtime(now)
year = timeStruct.tm_year
month = timeStruct.tm_mon
day = timeStruct.tm_mday
#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
date="{0}{1:02d}{2:02d}".format(year,month,day)
choliday=check_holiday.checkholiday(date)
holiday_status=choliday['work_status']
print('程序启动')

def job_gowork():
    print("开始上班打卡调度")
    second = random_minute(int(stagger_min))
    str_time = string_toDatetime(gowork_time, second)
    # print("程序启动，休眠{0}秒".format(second))
    msg = '今天是：{0}-{1:02d}-{2:02d},{3},将在{4}打卡'.format(year, month, day, choliday['wday'], str_time)
    print(msg)
    time.sleep(second)
    if holiday_status == 0:
        dingding = Ding.dingding(directory)
        png = dingding.goto_work()
        print(dingding.filename)
    else:
        print('今天不干活')


def job_offwork():
    print("开始下班打卡调度")
    if holiday_status == 0:
        dingding = Ding.dingding(directory)
        png = dingding.after_work()
        print(dingding.filename)
    else:
        print('今天不干活')

def random_minute(min):
    return random.randint(0,60*min)

def string_toDatetime(st,seconds):
    dt= datetime.datetime.strptime(st, "%H:%M")
    #print(dt)
    new_dt=dt+ datetime.timedelta(seconds=int('+{0}'.format(seconds)))
    str_dt=new_dt.strftime("%H:%M")
    print('随机到：',str_dt,'开始')
    return str_dt

schedule.every().day.at(gowork_time).do(job_gowork)
schedule.every().day.at(offwork_time).do(job_offwork)

while True:
    schedule.run_pending()

'''
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(10).seconds.do(run_threaded, job2)

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
'''