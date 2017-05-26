import requests
from bs4 import BeautifulSoup
import os

url = 'http://www.jianshu.com/'

page = 1

article_items = []

# 获取网页内容
def get_html(url):
    # 设置一些headers，要不捕捉不到数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    resp = requests.get(url, headers=headers)
    # 糗百有时候返回304，有时候返回200
    # 貌似是有段子更新的时候返回200，没有更新的时候返回304
    if resp.status_code in (200, 304):
        return resp
    else:
        return None

# 解析网页,获取需要的信息
def parse_html(resp):
    seen_snote_ids = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 结束判断条件
    isEnd = False if soup.find(name='ul', class_='note-list').find_all(name='li') else True
    for i in soup.find(name='ul', class_='note-list').find_all(name='li'):
        # items = []
        # 记录seen_snote_ids
        seen_snote_ids.append(i.get('data-note-id'))
        # print(i.get('data-note-id'))
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
        # if item not in article_items:
        article_items.append(item)
        print(item)
        # with open('jsHomePage2.txt', 'a') as f:
        #     for item in items:
        #         f.write(str(item) + os.linesep)
    # 翻页爬取
    id_data = '&seen_snote_ids%5B%5D='.join(seen_snote_ids)
    global page
    page = page + 1
    # 设置一些headers，要不捕捉不到数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Cookie': 'remember_user_token=W1s1Mjk4Mzg3XSwiJDJhJDEwJDEvSkNBcTNuUEg4Z0pMUlNwTXpqNE8iLCIxNDk1NTU0NTQ0LjQ2NjQzNDciXQ%3D%3D--00e5743d1005f1872b9658543d72184d2241ae12; _gat=1; _ga=GA1.2.1093563359.1495552752; _gid=GA1.2.1923847820.1495555456; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1495552752,1495554089,1495554286,1495554443; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1495555456; _session_id={}'.format(resp.cookies['_session_id']),
    }
    # print(headers)
    next_page_url = 'http://www.jianshu.com/?seen_snote_ids%5B%5D=' + id_data + '&page={}'.format(page)
    if page <= 20:
        print(next_page_url)
        parse_html(requests.get(next_page_url, headers=headers))

if __name__ == '__main__':
    parse_html(get_html(url))
    temp = article_items
    for i in article_items:
        if i not in temp:
            temp.append(i)
    with open('jsHomePage.txt', 'w') as f:
        # parse_html(get_html(url))
        for item in temp:
            f.write(str(item) + os.linesep)