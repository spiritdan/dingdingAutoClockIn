import holiday as holiday, DingDing as Ding
import time
import configparser
import check_holiday
config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg",encoding='utf-8')
directory = config.get("ADB","directory")

now = int(time.time())
timeStruct = time.localtime(now)
year = timeStruct.tm_year
month = timeStruct.tm_mon
day = timeStruct.tm_mday

#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
holiday_status= holiday.check_holiday(year, month, day)
date="{0}{1:02d}{2:02d}".format(year,month,day)
holiday_status=check_holiday.checkholiday(date)['work_status']
print(holiday_status)


if holiday_status==0:
    dingding = Ding.dingding(directory)
    dingding.goto_work()
    png =dingding.filename
    print(png)
else:
    print('今天不干活')
