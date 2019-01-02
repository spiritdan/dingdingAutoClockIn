import json
import time



with open('calendar.json', 'r') as f:
    calendar = json.load(fp=f)

def checkholiday(date):
    dict_calendar=calendar[date]
    return dict_calendar

if __name__ == "__main__":
    dict_calendar=checkholiday("20180106")
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