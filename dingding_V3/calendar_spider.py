# -*- coding:utf-8 -*-
import time
import requests
import bs4
import json
import sys
import copy
import os

# 工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
work_status = 0


def check_status(special_day, date, wday):
    if special_day:
        status = date.select('a')[0]['class']
        # print(status[0])
        if status[0] == 'wnrl_riqi_xiu':
            work_status = 2
        elif status[0] == 'wnrl_riqi_ban':
            work_status = 0
    else:
        # 普通日期分周末和工作日
        if wday in ['星期六', '星期日']:
            work_status = 1
        else:
            work_status = 0
    return work_status


date_dict = {}


def check_holiday(year):
    for month in range(1, 13):

        server_url = "https://wannianrili.51240.com/ajax/?q={0}-{1:02d}&v=18121802".format(year, month)
        vop_url_request = requests.get(server_url)

        # print(vop_url_request.text)
        bs = bs4.BeautifulSoup(vop_url_request.text, 'html.parser')
        # wnrl_riqi_ban表示休息日上班 wnrl_riqi_xiu表示公休日 其他周末和工作日无特别标志
        datelist = bs.select('.wnrl_riqi')
        datelist_details = bs.select('.wnrl_k_you')

        for i in range(len(datelist)):
            strdate = '{0}{1:02d}{2:02d}'.format(year, month, i + 1)
            print(strdate)
            special_day = datelist[i].find_all('a', {'class': {'wnrl_riqi_xiu', 'wnrl_riqi_ban'}})
            wday = datelist_details[i].select('.wnrl_k_you_id_biaoti')[0].getText().split()[-1]
            ddate = datelist[i]
            work_status = check_status(special_day, ddate, wday)
            print(work_status)
            temp_dict = {}
            temp_dict['work_status'] = work_status
            temp_dict['wday'] = wday
            # print(strdate,temp_dict)
            date_dict[strdate] = temp_dict

    print(date_dict)
    return date_dict


if __name__ == "__main__":
    # 日期改一下，内容是叠加的
    # python calendar_spider.py 2019
    #new_dict_calendar = check_holiday(sys.argv[1])
    print("如果网站改版了有可能无法爬去")
    new_dict_calendar=check_holiday('2019')
    if not os.path.exists('calendar.json'):
        with open('calendar.json', 'w+', encoding="utf-8") as touch:
            touch.close()

    with open('calendar.json', 'r+', encoding="utf-8") as f:
        try:
            dict_calendar = copy.deepcopy(json.loads(f.read()))
            f.seek(0)
            f.truncate()
            print(dict_calendar)
        except json.decoder.JSONDecodeError as e:
            dict_calendar = {}
            print('json格式错误')
        except FileNotFoundError:
            dict_calendar = {}
            os.mknod('calendar.json')
            print('json文件不存在')

        for k, v in new_dict_calendar.items():
            print(k, v)
            dict_calendar[k] = v
        json.dump(dict_calendar, f)
        f.close()
    # with open('calendar.json', 'w+') as f:
    #    json.dump(calendar, f)


