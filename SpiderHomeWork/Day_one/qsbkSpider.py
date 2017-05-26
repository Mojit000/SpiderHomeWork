import requests
from bs4 import BeautifulSoup
from random import choice

url = 'http://www.qiushibaike.com/text/'

# 获取网页内容
def get_html(url):
    resp = requests.get(url)
    html = resp.text
    # 糗百有时候返回304，有时候返回200
    # 貌似是有段子更新的时候返回200，没有更新的时候返回304
    if resp.status_code in (200, 304):
        return html
    else:
        return None

# 解析网页,获取需要的信息
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find_all(name='div', class_='mb15'):
        print({
            'author_name': i.find(name='h2').text,
            # 根据div节点的class属性来判断性别,匿名用户不知道性别
            # 节点信息<div class="articleGender manIcon">21</div>
            'author_sex': i.find(
                # get('class')获取到两个属性,一个是articleGender,另一个是manIcon(womanIcon)
                # get('class')[-1]取到manIcon(womanIcon)字符串后用切片取得man(woman)
                # get('class')[-1][:-4]表示取字符串第一个字符到倒数第5个字符,字符串最后一个字符串索引表示为-1
                name='div', class_='articleGender').get('class')[-1][:-4] if i.find(
                    name='div', class_='articleGender') is not None else '不知道',
            # 匿名用户不知道年龄
            'author_age': i.find(
                name='div', class_='articleGender').text if i.find(
                    name='div', class_='articleGender') is not None else '0',
            'joke_content': i.find(name='div', class_='content').text.strip(),
            'laugher_count': i.find(name='div', class_='stats').text.split()[0],
            'comment_count': i.find(name='div', class_='stats').text.split()[-2],
            })
    # 实现分页爬取（递归）
    next_page = soup.find(name='ul', class_='pagination').find_all(name='li')[-1]
    # 递归结束条件：没有找到下一页按钮表示到了最后一页，结束
    if next_page.find(name='span', class_='next'):
        next_page_url = 'http://www.qiushibaike.com' + next_page.find(name='a').get('href')
        parse_html(get_html(next_page_url))

if __name__ == '__main__':
    parse_html(get_html(url))