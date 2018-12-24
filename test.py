from bs4 import BeautifulSoup
import urllib.request
import re
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

#打开网址
response = urllib.request.urlopen('http://mall.gree.com/mall/zh-CN/zhuhai/KB276041200')

#读取页面
shuchu = response.read().decode('utf-8')

#提取标题
title = re.findall('<h1>(.*?)</h1>',shuchu)

#处理标题
title = (" ".join(title))
title = title.split(' ')

#产品名称
model_name = title[0]
print("产品名称为：{}".format(model_name))
#print(title)
print("================")

#获取网页
res = requests.get('http://mall.gree.com/mall/zh-CN/zhuhai/KB276041200')

#利用bs4解析网页
soup = BeautifulSoup(res.content,'lxml')

#根据父节点选择参数
result = soup.find_all(name = 'tr')

#列表强转字符串
str_result = str(result)

#选择提取内容
pattern = '\>(.*?)</td>'
results = re.findall(pattern, str_result)

#产品参数的属性类别
attribute = results[::2]
attribute = list(reversed(attribute))
attribute = attribute[8:]
attribute = list(reversed(attribute))

#产品参数的数值
parameter = results[1::2]
parameter = list(reversed(parameter))
parameter = parameter[8:]
parameter = list(reversed(parameter))

#主题类参数
attr_theme = attribute[:4]
para_theme = parameter[:4]
dic_theme = dict(map(lambda x,y:[x,y],attr_theme,para_theme))
print("主题类参数：\n")
for key,value in dic_theme.items():
    print('{} | {}'.format(key, value))
print("================\n")

#功能类参数
attr_func = attribute[5:16]
para_func = parameter[5:16]
dic_func = dict(map(lambda x,y:[x,y],attr_func,para_func))
print("功能类参数：\n")
for key,value in dic_func.items():
    print('{} | {}'.format(key, value))
print("================\n")

#规格类参数
attr_spec = attribute[17:24]
para_spec = parameter[17:24]
dic_spec = dict(map(lambda x,y:[x,y],attr_spec,para_spec))
print("规格类参数：\n")
for key,value in dic_spec.items():
    print('{} | {}'.format(key, value))
print("================\n")


#属性和数值合成为字典
dic = dict(map(lambda x,y:[x,y],attribute,parameter))
for key,value in dic.items():
    print('{} | {}'.format(key, value))

'''
print("================")
#按字典key查找对应的value
print(dic['系列'])

#输出字典所有的keys
print("字典的属性类别为：{}".format(dic.keys()))

#输出字典所有的values
print("字典的参数数值为：{}".format(dic.values()))
'''

print("================")
try:
    path = './'
    full_path = path + model_name + '.txt'
    fl=open(full_path, 'w')
    fl.write("主题参数为：")
    fl.write(json.dumps(dic_theme,ensure_ascii=False,indent=2))
    fl.write("\n\n功能类参数为：")
    fl.write(json.dumps(dic_func,ensure_ascii=False,indent=2))
    fl.write("\n\n规格类参数为：")
    fl.write(json.dumps(dic_spec,ensure_ascii=False,indent=2))
    fl.close()

    print("数据写入完成!")
except:
    pass
