import datetime

now=datetime.datetime.now()
year = now.year
month = now.month
day = now.day

date = datetime.datetime(year, month, day)
date =(date.strftime("%B%d%Y"))
print(date)
