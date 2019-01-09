# -*- coding: utf-8 -*-
import time,os
import schedule
import holiday as holiday, DingDing as Ding
import configparser
import check_holiday

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg", encoding='utf-8')
directory = config.get("ADB","directory")
gowork_time=config.get("time","go_time")
offwork_time=config.get("time","off_time")

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

dingding = Ding.dingding(directory)
dingding.goto_work()
png = dingding.filename
png_image='D:\\dingding\\' +png
print(png_image)
os.startfile(png_image)
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