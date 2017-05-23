import requests
from bs4 import BeautifulSoup
import os

url = 'http://www.jianshu.com/'

# 获取网页内容
def get_html(url):
    # 设置一些headers，要不捕捉不到数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    resp = requests.get(url, headers=headers)
    html = resp.text
    # 糗百有时候返回304，有时候返回200
    # 貌似是有段子更新的时候返回200，没有更新的时候返回304
    if resp.status_code == 200 or resp.status_code == 304:
        return html
    else:
        return None

# 解析网页,获取需要的信息
def parse_html(html):
    items = []
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find(name='ul', class_='note-list').find_all(name='li'):
        # 作者名称
        author_name = i.find(name='div', class_='name').find(name='a').text
        # 文章标题
        article_title = i.find(name='div', class_='content').find(name='a', class_='title').text
        # print(article_title)
        # 文章发表的时间
        article_release_time = i.find(name='span').get('data-shared-at').split('+')[0]
        # 文章是否有所投专题，如有
        # 说明：<div class="meta"></div>该标签的文字信息保存了阅读量，评论数，点赞数，打赏数，所投专题的信息
        # 可以通过i.find(name='div', class_='meta').text获得
        # 由于有没有所投专题会影响split()后的结果，如有，split()[0]表示的就是所投专题；如果没有，split()[0]表示的就是阅读量
        # 所以先判断是否有所投专题
        if i.find(name='div', class_='meta').find(name='a', class_='collection-tag'):
            # 文章阅读量
            article_read_count = i.find(name='div', class_='meta').text.split()[1]
            # 文章评论数
            article_comment_count = i.find(name='div', class_='meta').text.split()[2]
            # 文章点赞数
            article_likeit_count = i.find(name='div', class_='meta').text.split()[3]
            # 文章打赏数，打赏不一定有，所以也要先判断
            article_payit_count = '0' if len(i.find(name='div', class_='meta').text.split())<5 else i.find(name='div', class_='meta').text.split()[4]
            # 所投专题
            article_collection_tag = i.find(name='div', class_='meta').find(name='a', class_='collection-tag').text.split()[0]
        # 没有所投专题
        else:
            article_read_count = i.find(name='div', class_='meta').text.split()[0]
            article_comment_count = i.find(name='div', class_='meta').text.split()[1]
            article_likeit_count = i.find(name='div', class_='meta').text.split()[2]
            # 打赏数不一定有，所以要先判断
            article_payit_count = '0' if len(i.find(name='div', class_='meta').text.split())<5 else i.find(name='div', class_='meta').text.split()[4]
            article_collection_tag  = '没有收录到任何专题'
        item = [author_name, article_title, article_release_time, 
        article_read_count, article_comment_count, article_likeit_count, article_payit_count, article_collection_tag]
        items.append(item)     
    return items

if __name__ == '__main__':
    with open('jsHomePage.txt', 'w') as f:
        items = parse_html(get_html(url))
        for item in items:
            f.write(str(item) + os.linesep)