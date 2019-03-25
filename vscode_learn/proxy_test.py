response = ''
import time
import re
import requests
def get_proxy():
    '''
    实现代理IP的基本利用,代理IP的请求异常众多
    :return: 返回可能有效的代理IP
    '''
    global response
    # 代理IP的请求也需要考虑本身出错，比如请求过快，IP本身的问题 两个问题
    proxy_api = 'http://s.zdaye.com/?api=201809060931142252&count=1&px=2'
    try:
        response = requests.get(proxy_api)
        response.encoding = response.apparent_encoding
    except:
        print('IP访问出错，延时10s')
        time.sleep(10)
        get_proxy()

    print('IP1', response.text)
    proxy = {'http': response.text}
    pat = re.compile('<bad>请求过快，请再等(.*?)秒</bad>', re.S)
    result = re.search(pat, response.text)
    if result:
        # print(response.text)
        time.sleep(int(result.group(1)))
        # 再次请求
        try:
            response = requests.get(proxy_api)
        except:
            print('IP访问出错，延时10s')
            time.sleep(10)
            get_proxy()
        print('IP2', response.text)
        proxy = {'http': response.text}
        print(proxy)
        # 还需测试IP的有效性、
        try:
            test_response = requests.get('http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/1101111807030101', proxies=proxy, timeout=10)
            if test_response.status_code == 200:
                print('代理有效')
                return proxy
            else:
                print('代理IP无效，访问百度失败，延时10s重新请求')
                time.sleep(10)
                get_proxy()
        except:
            print('代理测试出错')
            get_proxy()

    else:
        return proxy
        # get_proxy()

# proxy = get_proxy()
# print(proxy)


def request_format(Request_headers):
    '''
    尝试做成模块每次导入即可
    :param Request_headers:
    :return:
    '''
    headers = {}
    pattern = re.compile('\\n(.*?): (.*?)\\n', re.S)
    times = Request_headers.count('\n') - 2
    while times >= 0:
        result = re.search(pattern, Request_headers)
        Request_headers = Request_headers[Request_headers.index('\n') + 2:]
        headers[result.group(1)] = result.group(2)
        times = times - 1
    return headers

header = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Host: jzsc.mohurd.gov.cn
Referer: http://jzsc.mohurd.gov.cn/dataservice/query/comp/compDetail/001607220057287483
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
'''
proxy_api = 'http://s.zdaye.com/?api=201809060931142252&count=1&px=2'
response = requests.get(proxy_api)
headers = request_format(header)
proxy = {"https": response.text}
print(proxy)
# 111.178.128.95:23564
# 114.238.125.179:894
# 119.180.133.196:8060
test_response = requests.get('http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/1101111807030101', headers=headers, proxies=proxy, timeout=120)
print(test_response.text)
print(test_response.status_code)

# 并不能解决IP代理问题，换一台机器尝试

# 原因似乎是因为 http https 颠倒了，即要用相反的http协议代理访问
# 有时候住建部访问失败更多地是网站本身的问题
