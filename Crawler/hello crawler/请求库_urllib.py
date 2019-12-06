# 我们首先了解一下 Urllib 库，它是 Python 内置的 HTTP 请求库，也就是说我们不需要额外安装即可使用，它包含四个模块：
# 第一个模块 request，它是最基本的 HTTP 请求模块，我们可以用它来模拟发送一请求，就像在浏览器里输入网址然后敲击回车一样，只需要给库方法传入 URL 还有额外的参数，就可以模拟实现这个过程了。
# 第二个 error 模块即异常处理模块，如果出现请求错误，我们可以捕获这些异常，然后进行重试或其他操作保证程序不会意外终止。
# 第三个 parse 模块是一个工具模块，提供了许多 URL 处理方法，比如拆分、解析、合并等等的方法。
# 第四个模块是 robotparser，主要是用来识别网站的 robots.txt 文件，然后判断哪些网站可以爬，哪些网站不可以爬的，其实用的比较少。

#四个模块以request请求模块为主，其他模块为辅，对网页进行GET和POST两种请求方式，常规请求，带参请求，设置代理等。
import urllib.request
import urllib.parse
import urllib.error

import socket

#我们先来获取一下Python官网的源码，使用read()方法打印网页的HTML，read出来的是字节流,需要decode一下
response = urllib.request.urlopen("http://www.python.org")
print(response.read().decode("utf-8"))

#然后我们来看一下response，到底是什么类型的数据
print(type(response)) #<class 'http.client.HTTPResponse'>
#HTTPResponse类型包含read()、readinto()、getheader(name)、getheaders()、fileno() 等方法和 msg、version、status、reason、debuglevel、closed 等属性。

#接下来我们看几个方法
print(response.status)               #200
print(response.getheaders())         #[('Server', 'nginx'), ('Content-Type', 'text/html; charset=utf-8'), ('X-Frame-Options', 'DENY'), ('Via', '1.1 vegur'), ('Via', '1.1 varnish'), ('Content-Length', '48537'), ('Accept-Ranges', 'bytes'), ('Date', 'Sat, 03 Aug 2019 07:30:08 GMT'), ('Via', '1.1 varnish'), ('Age', '1939'), ('Connection', 'close'), ('X-Served-By', 'cache-iad2140-IAD, cache-lax8644-LAX'), ('X-Cache', 'HIT, HIT'), ('X-Cache-Hits', '2, 144'), ('X-Timer', 'S1564817408.256143,VS0,VE0'), ('Vary', 'Cookie'), ('Strict-Transport-Security', 'max-age=63072000; includeSubDomains')]
print(response.getheader('Server'))  #nginx
#status属性可以得到返回值状态码  200代表请求成功，404代表网页未找到，500代表服务器内部错误
#getheaders方法可以可以获得响应的头信息。
#getherder传递一个server的参数得到的返回值是nginx，表示服务器使用nginx搭建

#data参数（post请求）
#data 参数是可选的，如果要添加 data，它要是字节流编码格式的内容，即 bytes 类型，通过 bytes() 方法可以进行转化，另外如果传递了这个 data 参数，它的请求方式就不再是 GET 方式请求，而是 POST。

#带参请求也就是POST请求，需要使用parse  urllib工具模块或者叫解析模块
data = bytes(urllib.parse.urlencode({"name":"hanxuan"}),encoding='utf-8')
response = urllib.request.urlopen("http://httpbin.org/post",data=data)
print(response.read().decode("utf-8"))

#timeout参数
#timeout 参数可以设置超时时间，单位为秒，意思就是如果请求超出了设置的这个时间还没有得到响应，就会抛出异常，如果不指定，就会使用全局默认时间。它支持 HTTP、HTTPS、FTP 请求。

#因为网页经常出现延迟相应问题，这里为了直观展示error模块效果，是指timeout为0.1。
try:
    response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')

# Request
#上面说了urlopen和一些简单的请求参数，但是要发出更高级的请求就需要Request方法。
url="http://www.python.org"

request = urllib.request.Request(url=url) #Rquest主要是将各种请求参数打包之后再使用urlopen发送请求。
response = urllib.request.urlopen(request)
print(response.read().decode("utf-8"))


#主要参数
#url：用于请求URL，必传参数
#data：如果要传，必须传bytes类型，如果它是字典，可以先用urllib.parse模块里的urlencode()编码
#headers：请求头，我们可以在构造请求时通过headers参数值构造，添加请求头最常用的用法就是通过修改User-Agent来伪装浏览器
#origin_req_host：指的是请求方的host名称或者IP地址
#unverifiable：这个请求是否是无法验证，默认False，即用户没用足够权限来选取接受这个请求的结果
#method：是一个字符串，用来只是请求的方法，比如：GET、POST、PUT等

url = 'http://httpbin.org/post'   # 请求URL
headers = {   # headers指定User-Agent，Host
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Host':'httpbin.org'
}
dict = {
    'name':'hanxuan'
}
data = bytes(urllib.parse.urlencode(dict), encoding='utf8')  # 参数转化为字节流
req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')  # 指定请求方式为POST
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))


#urllib.parse
#定义了url的标准接口，实现url的各种抽取
# parse模块的使用：url的解析，合并，编码，解码
# urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)：该函数用于解析 URL 字符串。程序返回一个 ParseResult 对象，可以获取解析出来的数据。
url = 'https://book.qidian.com/info/1004608738?wd=123&page=20#Catalog'
"""
url：待解析的url
scheme=''：假如解析的url没有协议,可以设置默认的协议,如果url有协议，设置此参数无效
allow_fragments=True：是否忽略锚点,默认为True表示不忽略,为False表示忽略
"""
result = urllib.parse.urlparse(url=url,scheme='http',allow_fragments=True)

print(result)
print("协议：",result.scheme)
print("域名：",result.netloc)
print("路径：",result.path)
print("参数：",result.params)
print("查询条件：",result.query)
print("锚点：",result.fragment)
"""
(scheme='https', netloc='book.qidian.com', path='/info/1004608738', params='', query='wd=123&page=20', fragment='Catalog')
scheme:表示协议
netloc:域名
path:路径
params:参数
query:查询条件，一般都是get请求的url
fragment:锚点，用于直接定位页
面的下拉位置，跳转到网页的指定位置
"""

# urllib.parse.urlunparse(parts)：该函数是上一个函数的反向操作，用于将解析结果反向拼接成 URL 地址。
url_parmas = ('https', 'book.qidian.com', '/info/1004608738', '', 'wd=123&page=20', 'Catalog')
#components:是一个可迭代对象，长度必须为6
result = urllib.parse.urlunparse(url_parmas)
print(result)
"""
https://book.qidian.com/info/1004608738?wd=123&page=20#Catalog
"""

# urllib.parse.quote()：将中文和URL编码互相转换
word = '中国梦'
url = 'http://www.baidu.com/s?wd='+urllib.parse.quote(word)
print(urllib.parse.quote(word))
print(url)

"""
%E4%B8%AD%E5%9B%BD%E6%A2%A6
http://www.baidu.com/s?wd=%E4%B8%AD%E5%9B%BD%E6%A2%A6
"""
unquote:可以将URL编码进行解码
url = 'http://www.baidu.com/s?wd=%E4%B8%AD%E5%9B%BD%E6%A2%A6'
print(urllib.parse.unquote(url))
"""
http://www.baidu.com/s?wd=中国梦
"""
# urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus)：将字典形式或列表形式的请求参数恢复成请求字符串。该函数相当于 parse_qs()、parse_qsl() 的逆函数。
parmas = {
    'wd':'123',
    'page':20
}
parmas_str = urllib.parse.urlencode(parmas)

print(parmas_str)

"""
page=20&wd=123
"""

#parse_qs()将url编码格式的参数反序列化为字典类型
parmas_str = 'page=20&wd=123'
parmas = urllib.parse.parse_qs(parmas_str)
print(parmas)

"""
{'page': ['20'], 'wd': ['123']}
"""

# urllib.parse.urljoin(base, url, allow_fragments=True)：该函数用于将一个 base_URL 和另一个资源 URL 连接成代表绝对地址的 URL。
base_url = 'https://book.qidian.com/info/1004608738?wd=123&page=20#Catalog'
sub_url = '/info/100861102'

full_url = urllib.parse.urljoin(base_url,sub_url)
print(full_url)


#urllib.error
#error的报错信息分为URLError和HTTPError。
#URLError是OSError的一个子类。有以下错误的时候错误信息就会被封装在URLError里：无网络；有网络但是由于种种原因导致服务器连接失败。
#而如果能够连接服务器但是服务器返回了错误代码如404，403等等（400以上），那么催无信息就会被封装在HTTPError里

# URLError与HttpError的区别：URLError封装的错误信息一般是由网络引起的，包括url错误；HTTPError封装的错误信息一般是服务器返回了错误状态码
# URLError与HttpError的关系：URLError是OSERROR的子类，HTTPError是URLError的子类

try:
    response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.HTTPError as e:
    print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
    print(e.reason)
else:
    print('Request Successfully')