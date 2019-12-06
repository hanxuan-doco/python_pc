# requests是python实现的最简单易用的HTTP库，建议爬虫使用requests
# requests是在urllib库上扩展的第三方库
import requests



#1、概述

#1.1、实例

# 发起GET请求
url = "https://www.python.org/"
response=requests.get(url=url)
# 查看响应类型  requests.models.Response
print(response)                 #<Response [200]>
print(type(response))           #<class 'requests.models.Response'>
# 输出状态码
print(response.status_code)     #200
# 输出响应内容类型   byte  text
print(type(response.content))
print(type(response.text))
# 输出响应内容
print(response.content)         #获取源码的字节流格式，一般用于获得图片和视频
print(response.text)            #获取源码的文本格式（如要对获取源码进行分析用这个）
# 输出编码格式
print(response.encoding)        #UTF-8
# 输出cookies
print(response.cookies)

#1.2、各种请求方式
# 发起POST请求
requests.post('http://httpbin.org/post')
# 发起PUT请求
requests.put('http://httpbin.org/put')
# 发起DELETE请求
requests.delete('http://httpbin.org/delete')
# 发送HEAD请求
requests.head('http://httpbin.org/get')
# 发送OPTION请求
requests.options('http://httpbin.org/get')



#2、请求

#2.1、带参请求

#2.1.1、get带参请求

#（1）？+参数（?key1=value1）
response1 = requests.get("http://httpbin.org/get?key1=value1")
print(response1.url)    #http://httpbin.org/get?key1=value1

#（2）parameter
parameter = {
            "key1":"value1",
            "key2":"value2"
            }
response2 = requests.get("http://httpbin.org/get",params = parameter)
print(response2.url)    # http://httpbin.org/get?key1=value1&key2=value2

#（3）还可以将一个列表作为值传入
parameter = {
            "key1":"value1",
            "key2":["value21","value22"]
}
response3 = requests.get("http://httpbin.org/get",params = parameter)
print(response3.url)    # http://httpbin.org/get?key1=value1&key2=value21&key2=value22

#（4）注意字典里值为 None 的键都不会被添加到 URL 的查询字符串里。
parameter = {
            "key1":"value",
            "key2":None
}
response4 = requests.get("http://httpbin.org/get",params = parameter)
print(response4.url)    #http://httpbin.org/get?key1=value


#2.1.2、post带参请求

#（1）传递一个字典类型数据
payload = {
    "key1":"value1",
    "key2":"value2"
}
response = requests.post("http://httpbin.org/post",data = payload)
print(response.text)

#（2）传递一个元祖类型数据
payload = (("key1","value1"),("key1","value2"))
response = requests.post("http://httpbin.org/post",data = payload)
print(response.text)


#2.2、解析json

response = requests.get('http://httpbin.org/get')
# 获取响应内容
print(type(response.text))
# 如果响应内容是json,就将其转为json
print(response.json())
# 输出的是字典类型
print(type(response.json()))


#2.3、定制请求头

#以知乎为例子
response =requests.get("https://www.zhihu.com")
print(response.text)    #报错

new_headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

response = requests.get("https://www.zhihu.com",headers = new_headers)
print(response.text)        #正常输出


#2.4、基本POST请求格式

# 设置传入post表单信息
data= { 'name':'hanxuan', 'age':20}
# 设置请求头信息
headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
}
# 设置请求头信息和POST请求参数(data)
response = requests.post('http://httpbin.org/post', data=data, headers=headers)
print(response.text)



#3、响应

#3.1、获得响应属性

response = requests.get('http://www.jianshu.com/')

# 获取响应状态码
print(type(response.status_code),response.status_code)
# 获取响应头信息
print(type(response.headers),response.headers)
# 获取响应头中的cookies
print(type(response.cookies),response.cookies)
# 获取访问的url
print(type(response.url),response.url)
# 获取访问的历史记录
print(type(response.history),response.history)




#4、高级操作


#4.1、文件上传

files = {'file': open('favicon.ico', 'rb')}
# 往POST请求头中设置文件(files)
response = requests.post('http://httpbin.org/post', files=files)
print(response.text)


#4.2、获取cookies

response = requests.get('http://www.python.org')
print(response.cookies)
for key, value in response.cookies.items():
    print(key, '=====', value)


# 4.3、会话维持

# 4.3.1、普通请求

requests.get('http://httpbin.org/cookies/set/number/12456')
response = requests.get('http://httpbin.org/cookies')
# 本质上是两次不同的请求，session不一致
print(response.text)

# 4.3.2、会话维持请求

# 从Requests中获取session
session = requests.session()
# 使用seesion去请求保证了请求是同一个session
session.get('http://httpbin.org/cookies/set/number/12456')
response = session.get('http://httpbin.org/cookies')
print(response.text)


# 4.4、证书验证

# 4.4.1、无证书访问

response = requests.get('https://www.12306.cn')
# 在请求https时，request会进行证书的验证，如果验证失败则会抛出异常
print(response.status_code)

# 4.4.2、关闭证书验证

# 关闭验证，但是仍然会报出证书警告
response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)

# 4.4.3、消除关闭证书验证的警告

from requests.packages import urllib3

# 关闭警告
urllib3.disable_warnings()
response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)

# 4.4.4、手动设置证书

# 设置本地证书
response = requests.get('https://www.12306.cn', cert=('/path/server.crt', '/path/key'))
print(response.status_code)


# 4.5、代理设置

# 4.5.1、设置普通代理

proxies = {
    "http": "http://127.0.0.1:9743",
    "https": "https://127.0.0.1:9743",
}
# 往请求中设置代理(proxies)
response = requests.get("https://www.taobao.com", proxies=proxies)
print(response.status_code)

# 4.5.2、设置带有用户名和密码的代理

proxies = {
    "http": "http://user:password@127.0.0.1:9743/",
}
response = requests.get("https://www.taobao.com", proxies=proxies)
print(response.status_code)

# 4.5.3、设置socks代理

import requests

proxies = {
    'http': 'socks5://127.0.0.1:9742',
    'https': 'socks5://127.0.0.1:9742'
}
response = requests.get("https://www.taobao.com", proxies=proxies)
print(response.status_code)


# 4.6、超时设置

from requests.exceptions import ReadTimeout

try:
    # 设置必须在500ms内收到响应，不然或抛出ReadTimeout异常
    response = requests.get("http://httpbin.org/get", timeout=0.5)
    print(response.status_code)
except ReadTimeout:
    print('Timeout')


# 4.7、认证设置

from requests.auth import HTTPBasicAuth

r = requests.get('http://120.27.34.24:9001', auth=HTTPBasicAuth('user', '123'))
#r = requests.get('http://120.27.34.24:9001', auth=('user', '123'))
print(r.status_code)


# 4.8、异常处理

from requests.exceptions import ReadTimeout, ConnectionError, RequestException

try:
    response = requests.get("http://httpbin.org/get", timeout=0.5)
    print(response.status_code)
except ReadTimeout:
# 超时异常
    print('Timeout')
except ConnectionError:
# 连接异常
    print('Connection error')
except RequestException:
# 请求异常
    print('Error')

