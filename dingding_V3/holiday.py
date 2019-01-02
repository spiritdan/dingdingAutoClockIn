# -*- coding:utf-8 -*-
import time
import requests
import bs4
#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
work_status=0

def check_holiday(year,month,day):
    server_url = "https://wannianrili.51240.com/ajax/?q={0}-{1:02d}&v=18121802".format(year,month)
    vop_url_request = requests.get(server_url)


    #print(vop_url_request.text)
    bs=bs4.BeautifulSoup(vop_url_request.text,'html.parser')
    #wnrl_riqi_ban表示休息日上班 wnrl_riqi_xiu表示公休日 其他周末和工作日无特别标志
    datelist=bs.select('.wnrl_riqi')
    datelist_details=bs.select('.wnrl_k_you')
    #print(datelist[day-1])
    special_day=datelist[day-1].find_all('a',{'class':{'wnrl_riqi_xiu','wnrl_riqi_ban'}})
    wday = datelist_details[day - 1].select('.wnrl_k_you_id_biaoti')[0].getText().split()[-1]
    print('今天是：{0}-{1}-{2} {3}'.format(year,month,day,wday))
    #判断是否为空,special_day表示是否被调休（法定节假日和被调休）
    if special_day:
        status=datelist[day-1].select('a')[0]['class']
        print(status[0])
        if status[0]=='wnrl_riqi_xiu':
            print('今天是公休日')
            work_status=2
        elif status[0]=='wnrl_riqi_ban':
            print('今天被调休了，得上班')
            work_status=0
    else:
        #普通日期分周末和工作日
        if wday in ['星期六','星期日']:
            print('今天是周末')
            work_status = 1
        else:
            print('今天得上班')
            work_status = 0
    #print(work_status)
    return work_status

if __name__ == "__main__":
    status = check_holiday(2019, 5, 2)
    print(status)

    # 获得当前时间时间戳
    now = int(time.time())
    timeStruct = time.localtime(now)
    year = timeStruct.tm_year
    day = timeStruct.tm_mday
    month = timeStruct.tm_mon
    status=check_holiday(year,month,day)
    print(status)