'''
    河北
    人员安全许可证
    http://www.hebjs.gov.cn/was5/web/search?page=2&channelid=293219&perpage=15&outlinepage=10&username=&zsbh=&qymc=
    内嵌网页，直接单独请求即可

'''

import re
import requests
import time
import pymysql
import random

db = pymysql.connect(host='localhost', user='root',
                     password='root', port=3306, db='lyp_prov')
cursor = db.cursor()


def request_format(Request_headers):
    headers = {}
    pattern = re.compile('\\n(.*?): (.*?)\\n', re.S)
    times = Request_headers.count('\n') - 2
    while times >= 0:
        result = re.search(pattern, Request_headers)
        Request_headers = Request_headers[Request_headers.index('\n') + 2:]
        headers[result.group(1)] = result.group(2)
        times = times - 1
    return headers


request_headers = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7
Connection: keep-alive
Cookie: JSESSIONID=95ABF85B7AD01ACFB790E66078AF747F
Host: www.hebjs.gov.cn
Referer: http://www.hebjs.gov.cn/was5/web/search?page=1&channelid=293219&perpage=15&outlinepage=10&username=&zsbh=&qymc=
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
'''

headers = request_format(request_headers)


def get_page(url):
    '''
    获取通用页面 
    :param url: 目标页面链接
    :return: html页面
    '''
    try:
        response = requests.get(url, headers, timeout=120)
        if response.status_code == 200:
            return response.text
        else:
            print('STATUS CODE ILLEGAL.')
            return -1
    except:
        print('REQUESTS ERROR.')
        return -1


def parse_data(html):
    # 意即空格 ' ' ? '\t' 似乎都是表示空格的.
    '''
    可以编写一个描述通用的解析函数，功能即解析需要的数据并返回字典列表
    参数：
    1. 正则表达式规则（str）
    2. 带解析的数据（str）
    '''
    pat = re.compile(
        '<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>', re.S)
    results = re.findall(pat, html)
    if results:
        certs = []
        for result in results:
            print('\\')
            cert_dict = {}
            cert_dict['person_name'] = result[0]
            cert_dict['cert_code'] = result[1]
            cert_dict['com_name'] = result[2]
            cert_dict['valid'] = result[3]
            print(cert_dict, end='\n')
            certs.append(cert_dict)
        return certs
    else:
        print('PARSE ERROR.')
        return -1


def save_data(certs):
    '''
    用于储存数据，可以编写一个描述通用的存储方法，有两个功能
    1 存储时检测带存储数据是否已经存在，如果存在就不存储
    2 存储相应数据 
    那么参数应该是哪些呢？  
    1. 数据表名称(str)
    2. 需要去重对比的字段名称  此处可能需要考虑多个字段名称的参数问题(*str)
    3. 需要存储的数据（dict）
    '''
    for cert_dict in certs:
        # repeat testing
        sql_rep = 'select cert_id from hebei_per_secur_lice where cert_code=\'{}\''.format(
            cert_dict['cert_code'])
        cursor.execute(sql_rep)
        one = cursor.fetchone()
        if one:
            continue
        else:
            # save new data
            table = 'hebei_per_secur_lice'
            keys = ','.join(cert_dict.keys())
            values = ','.join(['%s'] * len(cert_dict))
            sql_insert = 'INSERT INTO {table}}({keys}}) values({values}})'.format(
                table, keys, values)
            # 用元组解析即可
            cursor.execute(sql_insert, tuple(cert_dict.values()))
            db.commit()

# learn git and js. with python, also including crwaler.



def get_all():
    '''
    汇总函数，采集所有数据并存储
    '''
    MAX_PAGES = 13034
    page = 11458
    while page <= MAX_PAGES:
        print('Crawling data at ' + str(page) + ' pages.')
        url = 'http://www.hebjs.gov.cn/was5/web/search?page={}&channelid=293219&perpage=15&outlinepage=10&username=&zsbh=&qymc='.format(
            page)
        html = get_page(url)
        if html != -1:
            certs = parse_data(html)
            if certs != -1:
                save_data(certs)
        time.sleep(random.randint(1, 10))
        page += 1     
# 提交新的信息

get_all()


# 利用调试找出编写过程中的bug，然后在实际使用时就可以利用终端奔跑数
# 数据的采集，数据清晰，存储，然后关键是对数据的利用，比如数据分析，展示等

