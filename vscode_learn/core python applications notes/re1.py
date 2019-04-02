'''
一些RE学习笔记，因为RE过于迷人且强大，不知道比什么xpath,css-selector,pyquery强大到哪里去了
一些相对RE的简单深入学习BY《Python核心编程》
字符串模式匹配技术
'''
import re
'''
'.' 匹配除了'\n'的任意字符，当然可以利用特殊标记达到匹配所有字符的目的 re.S ???
'[]'  匹配某些单个的特定字符
'''
# 271097513@qq.com
# 正则匹配IP地址 192.168.1.1

# 那么更加严格的IP格式判断  需要判断： 0~255  即怎么用正则匹配出 0~255的数字


def _():
    pat = r'[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}'
    pat_ex = r'0|[1-9]{3}'
    _ex = '254.3.3.2'
    pat = re.compile(pat, re.S)
    result = re.search(pat, _ex)
    if result:
        print(result.group(0))

 
_()
