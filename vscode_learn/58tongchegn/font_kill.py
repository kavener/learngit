from fontTools.ttLib import TTFont

font = TTFont('58.ttf') # 打开本地的ttf文件
font.saveXML('58.xml')  # 转换成xml

import base64
import time

print(time.time())