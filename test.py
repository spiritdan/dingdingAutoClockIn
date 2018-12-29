import holiday as holiday, DingDing as Ding
import time
import configparser

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg")
directory = config.get("ADB","directory")

now = int(time.time())
timeStruct = time.localtime(now)
year = timeStruct.tm_year
month = timeStruct.tm_mon
day = timeStruct.tm_mday

#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
holiday_status= holiday.check_holiday(year, month, day)

if holiday_status==0:
    dingding = Ding.dingding(directory)
    dingding.goto_work()
    png =dingding.filename
    print(png)
else:
    print('今天不干活')