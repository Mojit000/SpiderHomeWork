import time
import datetime
import requests
import json
# timestamp =  time.time()

base_url ='http://d1.weather.com.cn/calendar_new/{year}/101300903_{date}.html?_='.format(year=2016, date=201605)
headers = {
    'Referer': 'http://www.weather.com.cn/weather40d/101300903.shtml',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}
datas = json.loads(requests.get(base_url.format(time.time()), headers=headers).content[11:])
for i in datas:
    print(i)
print(datetime.datetime.now().date())

url_date = ''