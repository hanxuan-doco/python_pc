# BeautifulSoup 是一个用于解析 HTML 文档的 Python 库，通过 BeautifulSoup，你只需要用很少的代码就可以提取出 HTML 中任何感兴趣的内容.
# 此外，它还有一定的 HTML 容错能力，对于一个格式不完整的HTML 文档，它也可以正确处理。
from bs4 import BeautifulSoup

#0、学习前知识

'''
<html>  
    <head>
     <title>hello, world</title>
    </head>
    <body>
        <h1>BeautifulSoup</h1>
        <p>如何使用BeautifulSoup</p>
    <body>
</html> 
'''
# 它由很多标签（Tag）组成，比如 html、head、title等等都是标签
# 一个标签对构成一个节点，比如 <html>...</html> 是一个根节点
# 节点之间存在某种关系，比如 h1 和 p 互为邻居，他们是相邻的兄弟（sibling）节点
# h1 是 body 的直接子（children）节点，还是 html 的子孙（descendants）节点
# body 是 p 的父（parent）节点，html 是 p 的祖辈（parents）节点
# 嵌套在标签之间的字符串是该节点下的一个特殊子节点，比如 “hello, world” 也是一个节点，只不过没名字。



#1.简单用法

text = """
<html>  
    <head>
     <title >hello, world</title>
    </head>
    <body>
        <h1>BeautifulSoup</h1>
        <p class="bold">如何使用BeautifulSoup</p>
        <p class="big" id="key1"> 第二个p标签</p>
        <a href="http://foofish.net">python</a>
    </body>
</html>  
"""
soup = BeautifulSoup(text, "html.parser")

# title 标签
print(soup.title)  #<title>hello, world</title>

# p 标签
print(soup.p)     #<p class="bold">如何使用BeautifulSoup</p>

# p 标签的内容
print(soup.p.string)    #如何使用BeautifulSoup


# 2、数据类型
# BeatifulSoup 将 HTML 抽象成为 4 类主要的数据类型。
# 分别是Tag , NavigableString , BeautifulSoup，Comment 。
# 每个标签节点就是一个Tag对象，NavigableString 对象一般是包裹在Tag对象中的字符串，BeautifulSoup 对象代表整个 HTML 文档。

print(type(soup))             #<class 'bs4.BeautifulSoup'>
print(type(soup.p))           #<class 'bs4.element.Tag'>
print(type(soup.p.string))    #<class 'bs4.element.NavigableString'>

# 2.1、Tag
# 每个 Tag 都有一个名字，它对应 HTML 的标签名称。

print(soup.h1.name)  #h1
print(soup.p.name)   #p


# 2.2、NavigableString
#获取标签中的内容，直接使用 .stirng 即可获取

print(soup.p.string)       #如何使用BeautifulSoup
print(type(soup.p.string)) #<class 'bs4.element.NavigableString'>



# 3、文档树操作

# 3.1、遍历文档树
# 遍历文档树，顾名思义，就是是从根节点 html 标签开始遍历，直到找到目标元素为止。
# 遍历的一个缺陷是，如果你要找的内容在文档的末尾，那么它要遍历整个文档才能找到它，速度上就慢了。

print(soup.body)
print(soup.body.p)
print(soup.body.p.string)

# 前面说了，内容也是一个节点，这里就可以用 .string 的方式得到。
# 遍历文档树的另一个缺点是只能获取到与之匹配的第一个子节点，例如，如果有两个相邻的 p 标签时，第二个标签就没法通过 .p 的方式获取.
# 这是需要借用 next_sibling 属性获取相邻且在后面的节点。


#3.2、搜索文档树
#搜索文档树是通过指定标签名来搜索元素，另外还可以通过指定标签的属性值来精确定位某个节点元素，最常用的两个方法就是 find 和 find_all。

#3.2.1、find_all
# find_all( name , attrs , recursive , text , **kwargs )
# find_all 的返回值是一个 Tag 组成的列表，方法调用非常灵活，所有的参数都是可选的。

#第一个参数name是标签节点的名字
print(soup.find_all("title"))
print(soup.find_all("p"))

#第二个参数attrs是class值
print(soup.find_all("p", "big"))    #等效于soup.find_all("p", class_="big")  因为 class 是 Python 关键字，所以这里指定为 class_。

#第五个参数kwargs是标签的属性名值对
print(soup.find_all(href="http://foofish.net"))
#同时他还支持正则
import re
print(soup.find_all(href=re.compile("^http")))
#属性除了可以是具体的值、正则表达式之外，它还可以是一个布尔值（True/Flase），表示有属性或者没有该属性。
print(soup.find_all(id="key1"))
print(soup.find_all(id=True))

#搜索和遍历相结合
#先定位到 body 标签，缩小搜索范围，再从 body 中找 a 标签。
body_tag = soup.body
print(body_tag.find_all("a"))

#3.2.2、find
# find 方法跟 find_all 类似，唯一不同的地方是，它返回的单个 Tag 对象而非列表，如果没找到匹配的节点则返回 None。如果匹配多个 Tag，只返回第0个。
print(body_tag.find("a"))
print(body_tag.find("p"))

#get_text()
# 获取标签里面内容，除了可以使用 .string 之外，还可以使用 get_text 方法.
# 不同的地方在于前者返回的一个 NavigableString 对象，后者返回的是 unicode 类型的字符串。

p1 = body_tag.find('p').get_text()
print(type(p1))
print(p1)

p2 = body_tag.find("p").string
print(type(p2))
print(p2)