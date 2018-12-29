# -*- coding:utf-8 -*-
import time
import requests
import bs4
#工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2；
work_status=0

def check_holiday(year):
    for month in range(1,13):
        server_url = "https://wannianrili.51240.com/ajax/?q={0}-{1:02d}&v=18121802".format(year,month)
        vop_url_request = requests.get(server_url)


        #print(vop_url_request.text)
        bs=bs4.BeautifulSoup(vop_url_request.text,'html.parser')
        #wnrl_riqi_ban表示休息日上班 wnrl_riqi_xiu表示公休日 其他周末和工作日无特别标志
        datelist=bs.select('.wnrl_riqi')
        datelist_details=bs.select('.wnrl_k_you')
        print(datelist)
        for i in range(len(datelist)):
            print(datelist[i])
            print()

if __name__ == "__main__":
    status=check_holiday(2019)
