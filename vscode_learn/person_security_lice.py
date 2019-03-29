import builtins
import numpy as np
'''
    河北
    人员安全许可证
    http://www.hebjs.gov.cn/was5/web/search?page=2&channelid=293219&perpage=15&outlinepage=10&username=&zsbh=&qymc=
    内嵌网页，直接单独请求即可

'''
import scrapy
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
    # 七月目标：当然最高目标是找到一份像智库二八六一的爬虫工程师的工作，那么我也可以降低目标在更短的时间去尝试熟悉市场需求，甚至找一份比现在薪资高些的工作啊
    # 不行，我不能妥协，要做就努力往好里做！ 我要达到的能力就是遇到需求可以拿出近似最优解！ 即能够得到一份满意的工作，10K以下的是我选择公司，而不是公司选我
    # 其实有很多需要或者可以锻炼的地方，而我就是懒得思考，只觉得做出来就行，而不是不断优化程序，重构，不断做到更优解，甚至思考其内部原理，设计模式，数据结构与算法等，这样怎么成为一名高手呢？
    # Python透析数据结构与算法（LeetCode） Python语言及面向对象（设计模式） Python并行编程及分布式架构（效率） Python爬虫（请求（requests，js，selenium，appnium...），解析（正则，Xpath，CSS-Selector， PyQuery...），Scrapy） MySQL（高性能存储）
    # 即从本质来看，爬虫仅仅是一个应用点，其根本还是Python、数据结构算法等内功、编程能力的修炼
    # 而我也确实佩服当初的高瞻远瞩，即从爬虫-数据分析-数据挖掘路线的精妙所在，当然我现在认识更加清楚，更加的起兴趣了，尤其是对技术的发展有了更加清晰而深刻的认识了
    # 即需要意识到学习是需要实践并总结复盘的，而不是一味的学习，这样只能学了忘浪费时间和精力，即学习方法
    # 那么就是需要一个长久且逐渐更正的安排，尤其是学习方法，自身习惯，还有自身，读书，兴趣，身体等等一个逐渐更正的过程，一个逐渐改变且不断坚持向上的过程，一个不断取得阶段性胜利的过程！
    #
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
    2. 需要去重对比的字段名称，此处可能需要考虑多个字段名称的参数问题(*str)
    3. 需要存储的数据(dict)
    '''
    for cert_dict in certs:
        # repeat testing
        sql_rep = 'select cert_id from hebei_per_secur_lice where cert_code=\'{}\''.format(
            cert_dict['cert_code'])
        cursor.execute(sql_rep)
        one = cursor.fetchone()
        if one:
            # 测试调试方法
            continue
        else:
            table = 'hebei_per_secur_lice'
            keys = ','.join(cert_dict.keys())
            values = ','.join(['%s'] * len(cert_dict))
            sql_insert = 'INSERT INTO {table}}({keys}}) values({values}})'.format(
                table, keys, values)
            # use tuple.
            cursor.execute(sql_insert, tuple(cert_dict.values()))
            db.commit()
# learn git and js. with python, also including crwaler. the most powerful git with vscode.


def get_all():
    '''
    by all. get all.
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
# commit new information.


# get_all()


# 利用调试找出编写过程中的bug，然后在实际使用时就可以利用终端奔跑数
# 数据的采集，数据清晰，存储，然后关键是对数据的利用，比如数据分析，展示等
# 提交所有已经暂存的修改，GIT确实是个强大的代码同步工具，我需要学着使用，尤其是自身的side project活动需要最大
# 其次是公司的代码可以直接提交私密仓库中以备份代码
# 使用多窗口管理不同项目


# 导入numpy

data2 = [[1, 2, 4], [2, 4, 5]]
print(data2)
arry1 = np.array(data2)
print(arry1)
# 缺点是不显示实体对象本身的方法
print(arry1.shape)
print(dir(builtins))
# 处理机制比较重要的


def f1():
    x = 99
    def f2():

        print(x)

    return f2
# f1()
# action()

# 工厂函数，实现了类似类的状态保存机制，而本质就是一个嵌套函数，利用变量保存所谓的“属性”
def maker(N):
    def action(X):
        return X ** N
    return action
f = maker(2)
print(f(3))

def fuc(N):
    # x = 4
    action = (lambda n: f(n) ** N)
    # 匿名函数表达式
    return action

action = fuc(2)
print(action(2))

class tester:
    def __init__(self, start):
        self.start = start
        # return start
    
    def nested(self, label):
        print(label, self.start)
        self.start += 1
F = tester(0)
F.nested('spam')

def f_args(**args):
    print(args)
f_args(h=2,r=3,c=4)
# 然后再实现一个动态解包，岂不是上天
# 函数本身的设计概念
