import json
import time
import configparser
import configparser
import os

config = configparser.ConfigParser(allow_no_value=False)
config.read("dingding.cfg", encoding='utf-8')
off_day = config.get("time","exception").split(",")
enable_calendar = config.get("time","enable_calendar")
try:
    with open('calendar.json', 'r') as f:
        calendar = json.load(fp=f)
except Exception as e:
    print('读取文件异常')
    calendar={}
def checkholiday(date):
    try:
        dict_calendar=calendar[date]
    except Exception as e:
        print(e)
        print("日历读取失败，切为手动设置模式")
        if date in off_day:
            dict_calendar={'work_status': 2, 'wday': '今天设置为休息日'}
        else:
            dict_calendar = {'work_status': 0, 'wday': '今天设置为上班打卡'}
    if enable_calendar.lower() == 'false':
        print('选择为手动设置休息日模式')
        if date in off_day:
            dict_calendar={'work_status': 2, 'wday': '今天设置为休息日'}
        else:
            dict_calendar = {'work_status': 0, 'wday': '默认设置为上班打卡'}
    return dict_calendar

if __name__ == "__main__":
    dict_calendar=checkholiday("20190109")
    print(dict_calendar)
    '''
    now = int(time.time())
    timeStruct = time.localtime(now)
    year = timeStruct.tm_year
    month = timeStruct.tm_mon
    day = timeStruct.tm_mday

    # 工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
    date = "{0}{1:02d}{2:02d}".format(year, month, day)
    dict_calendar=checkholiday(date)
    print(dict_calendar)
'''