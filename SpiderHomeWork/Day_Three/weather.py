import time
import datetime
from datetime import date
import requests
import json
import csv


base_url ='http://d1.weather.com.cn/calendar_new/{year}/{city_id}_{date}.html?_='

headers = {
    'Referer': 'http://www.weather.com.cn/weather40d/101300903.shtml',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

# 请求url，等到response
def get_html(url):
    return requests.get(url, headers=headers)

# datas = json.loads(get_html(base_url).content[11:])
# for i in datas:
#     print(i)

from datetime import timedelta

month = date.today().month
year = date.today().year
print(str(month).zfill(2))
print(str(year))

# 得到今天的日期：年、月
def get_today():
    today = {}
    year = date.today().year
    month = date.today().month
    today['year'] = year
    today['month'] = month
    return today

# 得到一年前的日期：年、月
def get_one_year_ago():
    one_year_ago = {}
    today = get_today() 
    one_year_ago['year'] = today.get('year') - 1
    one_year_ago['month'] = today.get('month')
    return one_year_ago

# 根据年、月的信息生成url列表
def generate_url_list(start_date, end_date, city_id = 101300903):
    weather_url_list = []
    dates = []
    for year  in range(start_date.get('year'), end_date.get('year') + 1):
        if year == end_date.get('year'):
            for month in range(1, start_date.get('month') + 1):
                date = {
                    'year': str(year),
                    'month': str(month).zfill(2)
                }
                dates.append(date)
        else:
            for month in range(start_date.get('month'), 12 + 1):
                date = {
                    'year': str(year),
                    'month': str(month).zfill(2)
                }
                dates.append(date)
    for date in dates:
        weather_url_list.append(
            base_url.format(
                year=date.get('year'), date=date.get('year') + date.get('month'), city_id = city_id)
                )
    return weather_url_list

# 清洗数据，将清洗后的数据保存成csv文件
def parser_weather_data(resp):
    weather_infos = json.loads(resp[11:])
    for info in weather_infos:
        with open('weather_beiliu.csv', 'a') as  csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [info.get('date'), info.get('hgl'), info.get('hmax'), info.get('hmin'), info.get('nlyf') + info.get('nl'), info.get('wk')])


def main():
    with open('weather_beiliu.csv', 'w') as  csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['日期', '降水概率', '最高温', '最低温', '农历', '星期几'])
    # 遍历url，获取天气预报信息
    for url in generate_url_list(get_one_year_ago(), get_today()):        
        request_url = url + str(round(time.time()*1000))
        # 提醒信息
        print('获取页面：{}的数据'.format(request_url))
        parser_weather_data(get_html(request_url).content)
        time.sleep(1)

if __name__ == '__main__':
    main()
