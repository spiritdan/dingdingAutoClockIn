import schedule
import time
import holiday as holiday, DingDing as Ding
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
holiday_status= holiday.check_holiday(year, month, day)


def job_gowork():
    print("开始上班打卡调度")
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