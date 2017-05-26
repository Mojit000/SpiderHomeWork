import requests
from bs4 import BeautifulSoup
import math
import re
import os

start_url = 'http://guba.eastmoney.com/list,meigu_1.html'

url = "http://guba.eastmoney.com/news,meigu,646708357.html"

base_url = "http://guba.eastmoney.com"
article_info = {}
# comments = []
# comments_url = []

# 获取所有帖子的信息
def get_articles_info(start_url):
    resp = get_html(start_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    page_data = soup.find(name='span', class_='pagernums').get('data-pager').split('|')
    page_nums = math.ceil(int(page_data[1]) / int(page_data[2]))
    print('共{}页'.format(page_nums))
    articles_infos = []
    for i in range(1, page_nums+1):
        print('爬取第{}页...'.format(i))
        articles_url = start_url.split('_')[0] + '_' + str(i) + '.html'
        article_infos = parser_articles_info(articles_url)
        with open('美股吧.txt', 'a') as f:
            for info in article_infos:
                f.write(str(info) + os.linesep)
        articles_infos.extend(article_infos)
    return articles_infos

# 获取一页的所有帖子信息：阅读量、评论数、发布时间、帖子的url、帖子的标题、帖子的所有评论
# param：每一页帖子的链接
def parser_articles_info(article_list_url):
    resp = get_html(article_list_url)
    articles_soup = BeautifulSoup(resp.text, 'html.parser')
    articles_infos = articles_soup.find_all(name='div', class_='articleh')
    articles = []
    for info in articles_infos:
        if '/news' in info.find(name='span', class_='l3').find(name='a').get('href'):
            article_infos = {
                'read_count': info.find(name='span', class_='l1').text,
                'reply_count': info.find(name='span', class_='l2').text,
                'release_time': info.find(name='span', class_='l5').text,
                'article_url': base_url + info.find(name='span', class_='l3').find(name='a').get('href'),
                'article_title': info.find(name='span', class_='l3').find(name='a').get('title'),
                'article_comments': parse_comment_page(get_html(base_url + info.find(name='span', class_='l3').find(name='a').get('href')))
            }
            articles.append(article_infos)
    # print(articles)
    return articles


# 根据url获取html文档
def get_html(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
         }
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp
    return None

# 解析帖子的html文档，提取需要的数据：帖子的内容以及帖子的所有评论
def parse_comment_page(resp):
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 正则表达式获取总的评论数
    pattern = re.compile(r'var pinglun_num=(.*?);')
    # 文章评论数
    article_info['reply_count'] = int(re.search(pattern, resp.text).group(1))
    # 文章内容
    article_info['article_content'] = soup.find(name='div', class_='stockcodec').text.strip()
    # print(article_info['article_content'])
    page_num = math.ceil(article_info['reply_count'] / 30)
    print('{}条评论'.format(article_info['reply_count'] ), ',', '共{}页'.format(page_num))
    # 爬取所有的评论
    article_comments = []
    if article_info['reply_count'] > 0:        
        for i in range(1, page_num+1):
            comment_url = '.'.join(resp.url.split('.')[:-1]) + '_{}'.format(i) + '.html'
            print(comment_url)
            article_comments.extend(parser_article_comment(comment_url))
    else:
        article_comments.append('本帖子暂时没有评论内容')
    return article_comments

# 获得帖子一页的评论信息
def parser_article_comment(comment_list_url):
    resp = get_html(comment_list_url)
    if resp:
        comment_soup = BeautifulSoup(resp.text, 'html.parser')
        comments_infos = comment_soup.find_all(name='div', class_='zwlitxt')
        comments = []
        # print(len(comments_infos))
        for info in comments_infos:
            comment = {}
            comment['commentator'] = info.find(name='span', class_='zwnick').find('a').text if info.find(name='span', class_='zwnick').find('a') else None
            comment['reply_time'] = info.find(name='div', class_='zwlitime').text
            comment['reply_content'] = info.find(name='div', class_='zwlitext').text
            comments.append(comment)
    return comments

def main():
    # resp = get_html(url)
    # parse_page(resp)
    # 帖子内容的列表，帖子的内容是一个字典类型
    infos = get_articles_info(start_url)
    print(len(infos))
    # for info in infos:
    #     info['comments'] = parse_comment_page(get_html(info.get('article_url')))
    #     print(info['comments'])
    # with open('meiguba.txt', 'w') as f:
    #     for info in infos:
    #         f.write(str(info) + os.linesep)

if __name__ == '__main__':
    main()

