# 正则表达式语言相对小型和受限（功能有限），因此并非所有字符串处理都能用正则表达式完成。
# 当然也有些任务可以用正则表达式完成，不过最终表达式会变得异常复杂。碰到这些情形时，编写
# Python 代码进行处理可能反而更好；尽管 Python 代码比一个精巧的正则表达式要慢些，但它更易理解。
import re



#0、常用方法

# re.compile: 编译一个正则表达式模式(pattern)
# re.match: 从头开始匹配, 使用group()方法可以获取第一个匹配值
# re.search: 用包含方式匹配，使用group()方法可以获取第一个匹配值
# re.findall: 用包含方式匹配，把所有匹配到的字符放到以列表中的元素返回多个匹配值
# re.sub: 匹配字符并替换
# re.split: 以匹配到的字符当做列表分隔符，返回列表



#1、基本模式

#1.1、简单字符
#没有特殊意义的字符都是简单字符，简单字符就代表自身，绝大部分字符都是简单字符，举个例子

# /abc/ // 匹配 abc
# /123/ // 匹配 123
# /-_-/ // 匹配 -_-

#1.2、转义字符
# 第一种，是为了匹配不方便显示的特殊字符，比如换行，tab符号等
# 第二种，正则中预先定义了一些代表特殊意义的字符，比如\w等
# 第三种，在正则中某些字符有特殊含义(比如下面说到的)，转义字符可以让其显示自身的含义

#具体看附表一

#1.3、字符集合
# 有时我们需要匹配一类字符，字符集可以实现这个功能，字符集的语法用[]分隔，下面的代码能够匹配a或b或c
# [abc]

# 如果要表示字符很多，可以使用-表示一个范围内的字符，下面两个功能相同
# [0123456789]
# [0-9]

# 在前面添加^，可表示非的意思，下面的代码能够匹配abc之外的任意字符
# [^abc]

# 其实正则还内置了一些字符集，在上面的转义字符有提到，下面给出内置字符集对应的自定义字符集
# . 匹配除了换行符（\n）以外的任意一个字符 = [^\n]
# \w = [0-9a-Z_]
# \W = [^0-9a-Z_]
# \s = [ \t\n\v]
# \S = [^ \t\n\v]
# \d = [0-9]
# \D = [^0-9]

#1.4、量词
# 如果我们有三个苹果，我们可以说自己有个3个苹果，也可以说有一个苹果，一个苹果，一个苹果，每种语言都有量词的概念
# 如果需要匹配多次某个字符，正则也提供了量词的功能，正则中的量词有多个，如?、+、*、{n}、{m,n}、{m,}

# {n}匹配n次，比如a{2}，匹配aa
# {m, n}匹配m-n次，优先匹配n次，比如a{1,3}，可以匹配aaa、aa、a
# {m,}匹配m-∞次，优先匹配∞次，比如a{1,}，可以匹配aaaa...
# ?匹配0次或1次，优先匹配1次，相当于{0,1}
# +匹配1-n次，优先匹配n次，相当于{1,}
# *匹配0-n次，优先匹配n次，相当于{0,}

# 正则默认和人心一样是贪婪的，也就是常说的贪婪模式，凡是表示范围的量词，都优先匹配上限而不是下限
# a{1, 3} // 匹配字符串'aaa'的话，会匹配aaa而不是a

# 有时候这不是我们想要的结果，可以在量词后面加上?，就可以开启非贪婪模式
# a{1, 3}? // 匹配字符串'aaa'的话，会匹配a而不是aaa

#1.5、字符边界
# 有时我们会有边界的匹配要求，比如已xxx开头，已xxx结尾

# ^在[]外表示匹配开头的意思
# ^abc // 可以匹配abc，但是不能匹配aabc

# $表示匹配结尾的意思
# abc$ // 可以匹配abc，但是不能匹配abcc

# 上面提到的\b表示单词的边界
# abc\b // 可以匹配 abc ，但是不能匹配 abcc

#1.6、选择表达式
# 有时我们想匹配x或者y，如果x和y是单个字符，可以使用字符集，[abc]可以匹配a或b或c，如果x和y是多个字符，字符集就无能为力了，此时就要用到分组

# 正则中用|来表示分组，a|b表示匹配a或者b的意思
# 123|456|789 // 匹配 123 或 456 或 789

#1.7、分组和引用

# 分组是正则中非常强大的一个功能，可以让上面提到的量词作用于一组字符，而非单个字符，分组的语法是圆括号包裹(xxx)
# (abc){2} // 匹配abcabc

# 分组不能放在[]中，分组中还可以使用选择表达式
# (123|456){2} // 匹配 123123、456456、123456、456123

# 和分组相关的概念还有一个捕获分组和非捕获分组，分组默认都是捕获的，在分组的(后面添加?:可以让分组变为非捕获分组，非捕获分组可以提高性能和简化逻辑
# '123'.match(/(?123)/) // 返回 ['123']
# '123'.match(/(123)/)  // 返回 ['123', '123']

# 和分组相关的另一个概念是引用，比如在匹配html标签时，通常希望<xxx></xxx>后面的xxx能够和前面保持一致
# 引用的语法是\数字，数字代表引用前面第几个捕获分组，注意非捕获分组不能被引用
# <([a-z]+)><\/\1> // 可以匹配 `<span></span>` 或 `<div></div>`等

#1.8、预搜索
# 如果你想匹配xxx前不能是yyy，或者xxx后不能是yyy，那就要用到预搜索

# js只支持先行预搜索，也就是xxx前面必须是yyy，或者xxx前面不能是yyy
# (?=1)2 // 可以匹配12，不能匹配22
# (?!1)2 // 可有匹配22，不能匹配12

#1.9、修饰符

# 默认正则是区分大小写，这可能并不是我们想要的，正则提供了修饰符的功能，修复的语法如下
# /xxx/gi // 最后面的g和i就是两个修饰符

# g正则遇到第一个匹配的字符就会结束，加上全局修复符，可以让其匹配到结束
# i正则默认是区分大小写的，i可以忽略大小写
# m正则默认遇到换行符就结束了，不能匹配多行文本，m可以让其匹配多行文本

#2、主要方法

#2.1、re.compile方法
# compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用。
# 其函数包含两个参数，一个pattern，一个可选参数flags。

#2.1.1、 参数
# re.compile(pattern[, flags])

# pattern : 一个字符串形式的正则表达式
# flags : 可选，表示匹配模式，比如忽略大小写，多行模式等，具体参数为：
# re.I 忽略大小写
# re.L 表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境
# re.M 多行模式
# re.S 即为 . 并且包括换行符在内的任意字符（. 不包括换行符）
# re.U 表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于 Unicode 字符属性数据库
# re.X 为了增加可读性，忽略空格和 # 后面的注释

# 上述flags re.I和re.M是非常常用的。如果要同时使用两个flags，可以使用re.I | re.M。

#2.1.2、例子

# 我们编写了一个电子邮箱的正则表达式，并用它来验证用户输入的邮箱是否有效。

email_pattern = re.compile(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$')
print(re.match(email_pattern, 'django@pyghon.org'))
print(re.match(email_pattern, '1009070053@qq.com'))



#2.2、re.match和re.search方法
# re.match和re.search方法类似，唯一不同的是re.match从头匹配，re.search可以从字符串中任一位置匹配。
# 如果有匹配对象match返回，可以使用match.group()提取匹配字符串。

#2.2.1、 参数
# re.match(pattern, string)
# re.search(pattern, string)

# pattern : 一个字符串形式的正则表达式
# string : 要匹配的字符串

#2.2.2、实例


# 编写了一个年份的正则表达式

year_pattern = re.compile(r'\d{4}') # 四位整数，匹配年份
string1 = '我爱1998和1999年'
match1 = re.match(year_pattern, string1)
print(match1)

match2 = re.search(year_pattern, string1)
print(match2)
print(match2.group())

# 你可以看到re.match没有任何匹配，而re.search也只是匹配到1998年，而没有匹配到1999年。这是为什么呢？
# re.match是从头匹配的，从头没有符合正则表达式，就返回None。
# re.search方法虽然可以从字符串任何位置开始搜索匹配，但一旦找到第一个匹配对象，其就停止工作了。


# 下例展示了我们如何从"Elephants are bigger than rats"里提取Elephants和bigger两个单词

string3 = "Elephants are bigger than rats";
match3 = re.search( r'(.*) are (.*?) .*', string3, re.M|re.I)

print(match3.group())
print(match3.group(1))
print(match3.group(2))

#match.group的编号是从1开始的，而不是像列表一样从0开始。


#有的符号如", ', )本身就有特殊的含义，我们在正则表达中使用时必需先对它们进行转义，方法就是在其符号前件反斜杠\。
#下例展示了我们如何从“总共楼层(共7层)"提取共7层三个字，我们需要给括号转义。

string4 = "总共楼层(共7层)"
pattern5 = re.compile(r'\(.*\)')

match5 = re.search(pattern5, string4)
print(match5.group())

pattern6 = re.compile(r'\((.*)\)')

match6 = re.search(pattern6, string4)
print(match6.group())
print(match6.group(1))

#我们pattern5和pattern6中都对外面双括号都加了反斜杠\，表明这是括号符号本身。
#在pattern6中我们还使用了一对没加反斜杠的括号，表明这是一个match group。


# 如果我们有”总共楼层(共7层)干扰)楼层"这样的字符串，加了个干扰问号，那我们该如何匹配(共7层)呢？

string10 = "总共楼层(共7层)干扰)问号"
pattern10 = re.compile(r'\(.*\)') # 默认贪婪模式
pattern11 = re.compile(r'\(.*?\)') # 加问号?变非贪婪模式

print(re.search(pattern10, string10).group())
print(re.search(pattern11, string10).group())

# Python里正则匹配默认是贪婪的，总是尝试匹配尽可能多的字符。
# 非贪婪的则相反，总是尝试匹配尽可能少的字符。如果要使用非贪婪模式，我们需要在., *, ?号后面再加个问好?即可。



#2.3、re.findall方法
# 试图从一个字符串中提取所有符合正则表达式的字符串列表时需要使用re.findall方法。
# findall方法使用方法有两种，一种是pattern.findall(string) ，另一种是re.findall(pattern, string)。
# re.findall方法经常用于从爬虫爬来的文本中提取有用信息。

#2.3.1、参数
# pattern.findall(string)
# re.findall(pattern, string)

# pattern : 一个字符串形式的正则表达式
# string : 要匹配的字符串

#2.3.2、实例

# 例1: pattern.findall(string) - 提取年份列表

year_pattern = re.compile(r'\d{4}') # 四位整数，匹配年份
string1 = '我爱1998和1999年'
print(year_pattern.findall(string1))



# 例2: re.findall(pattern, string) - 提取百度首页带有链接的关键词

import requests
response = requests.get('https://www.baidu.com')
response.encoding="utf-8"
urls = re.findall(r'<a.*>(.*)</a>', response.text,) # 获取带链接的关键词
for url in urls:
    print(url)



#2.4、re.sub方法
# 该方法经常用于去除空格，无关字符或隐藏敏感字符。

#2.4.1、参数
# re.sub(pattern, new_string, current_string)

# pattern : 一个字符串形式的正则表达式
# new_string : 要替换的字符串
# current_string : 要匹配的字符串

#2.4.2、实例

# 下例展示了如何把年份替换为****

year_pattern = re.compile(r'\d{4}') # 四位整数，匹配年份
string1 = '我爱1998和1999年'
replaced_str = re.sub(year_pattern, '****', string1)
print(replaced_str)



#2.5、re.split方法
#split方法用于分割字符串，但是并不完美

#2.5.1、参数
# re.split(pattern, string)

# pattern : 一个字符串形式的正则表达式
# string : 要匹配的字符串

#2.5.2、实例

# 下例分割后的字符串列表

string1 = "1cat2dogs3cats4"
list1 = re.split(r'\d+', string1)
print(list1)

# 列表首尾都多了空格，需要手动去除。