import requests 
import json
import re
import sqlite3

def create_table() :
    conn = sqlite3.connect('./keydata.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ArticleInfo(Article_Id INTEGER);")
    conn.close()

def db_get_articleid():
    conn = sqlite3.connect('./keydata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Article_Id FROM ArticleInfo ORDER BY Article_Id LIMIT 1;')
    
    rows = cursor.fetchone()
    if rows == None :
        rows = 0
    else :
        rows = rows[0]
    # print('db_get_articleid : {0}'.format(rows))
    return rows

def db_set_articleid(article_id):
    conn = sqlite3.connect('./keydata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Article_Id FROM ArticleInfo ORDER BY Article_Id LIMIT 1;')
    
    rows = cursor.fetchone()
    if rows != None :
        cursor.execute('DELETE FROM ArticleInfo;')
        
    # print('db_set_articleid : {0}'.format(article_id))
    cursor.execute('INSERT INTO ArticleInfo VALUES(:Article_Id);', {"Article_Id":article_id})
    
    conn.commit()
    conn.close()

def clean_html(raw_html) :
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def send_slackmessage_keyword(msg) :
    payload = { 'text' : msg }
    rsp = requests.post('https://hooks.slack.com/services/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', json=payload )


def get_querydata() :
    # 오크돔 검색 URI
    rsp = requests.get('https://apis.naver.com/cafe-web/cafe-mobile/CafeMobileWebArticleSearchListV2?cafeId=20486145&query=%EC%98%A4%ED%81%AC%EB%8F%94&searchBy=0&sortBy=date&page=1&perPage=50&adUnit=MW_CAFE_BOARD&ad=true').json()

    sts = rsp['message']['status']
    tot_cnt = rsp['message']['result']['articleCount']

    article_id = db_get_articleid()

    for i in range(0, tot_cnt) :
        j = tot_cnt - i
        if rsp['message']['result']['articleList'][j]['type'] == 'ARTICLE' :
            
            if '교환' not in clean_html(rsp['message']['result']['articleList'][j]['item']['subject']):
                if '삽니다' not in clean_html(rsp['message']['result']['articleList'][j]['item']['subject'])  :
                    if '구' not in clean_html(rsp['message']['result']['articleList'][j]['item']['subject'])  :
                        if '카푸' in clean_html(rsp['message']['result']['articleList'][j]['item']['subject'])  :
                            if article_id  < rsp['message']['result']['articleList'][j]['item']['articleId'] :
                                # print('제목 :{0}, ID : {1} , cost : {2} '.format(clean_html(rsp['message']['result']['articleList'][j]['item']['subject']), rsp['message']['result']['articleList'][j]['item']['articleId'],  rsp['message']['result']['articleList'][j]['item']['productSale']['cost'] ))
                            
                                article_id = rsp['message']['result']['articleList'][j]['item']['articleId']
                                db_set_articleid(article_id)
                                msg = '판매글 : ' + clean_html(rsp['message']['result']['articleList'][j]['item']['subject']) 
                                msg += '\n 시간 : ' + rsp['message']['result']['articleList'][j]['item']['currentSecTime']
                                msg += '\n 가격 : ' +  rsp['message']['result']['articleList'][j]['item']['productSale']['cost'] + '원'
                                msg += '\n 링크 : ' +  'https://m.cafe.naver.com/ca-fe/web/cafes/20486145/articles/' + str(rsp['message']['result']['articleList'][j]['item']['articleId'])
                                # print(msg)
                                send_slackmessage_keyword(msg)

# if __name__ == "__main__" : 
#     create_table()
#     while True :
#         get_querydata()
#     sleep(10)

 