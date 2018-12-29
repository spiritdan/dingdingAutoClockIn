import json

with open('calendar.json', 'r') as f:
    calendar = json.load(fp=f)

def checkholiday(date):
    dict_calendar=calendar[date]
    return dict_calendar

if __name__ == "__main__":
    dict_calendar=checkholiday("20181231")
    print(dict_calendar)
