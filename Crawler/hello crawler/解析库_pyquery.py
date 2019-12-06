# print('\n'.join([''.join([('JHSLOVEYXT!'[(x-y)%11]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-50,50)])for y in range(15,-15,-1)]))

#如果感觉正则书写太过麻烦，beatifulsoup语法过于繁琐，那么pyquery是一个很好的选择。
from pyquery import PyQuery as pq

#0、简单应用

# 声明了一个长HTML字符串，当作参数传递给PyQuery，这样就成功完成了初始化。
# 然后接下来将初始化的对象传入CSS选择器，在这个实例中我们传入li节点，这样就可以选择所有的li节点，打印输出可以看到所有的li节点的HTML文本。
html = '''
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
doc=pq(html)
print(doc("li"))

#除了HTML长字符串，还可以声明url来初始化
doc=pq(url="http://www.baidu.com")
print(doc("head"))#输出head标签

#还可以传递本地html文件
doc=pq(filename="文件名")
print(doc("head"))#输出head标签


#1、css选择器
# 在 CSS 中，选择器是一种模式，用于选择需要添加样式的元素。

#1.1、初始化对象
html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''


# 1.2、传入了一个CSS选择器，#container .list li，意思是选取id为container的节点内部的class为list的节点内部的所有li节点。

doc=pq(html)
print(doc("#container .list li"))



#2、查找元素
# 下面我们介绍一些常用的查询函数，这些函数和jQuery中的函数用法也完全相同。


#2.1、子元素
#2.1.1、find()
# 查找子节点需要用到find()方法，传入的参数是CSS选择器，我们还是以上面的HTML为例。可以使用层层嵌套的方式.
doc=pq(html)
items=doc(".list")
print(type(items))
print(items)

list=items.find("li")
print(type(list))
print(list)

# 首先我们选取了class为list的节点，然后我们调用了find()方法，传入了CSS选择器，选取其内部的li节点，最后都打印输出即可观察到对应的查询结果.
# 可以发现find()方法会将符合条件的所有节点选择出来，结果的类型是PyQuery类型。


# 2.1.2、children()
# 其实find()的查找范围是节点的所有子孙节点，而如果我们只想查找子节点，那可以用children()方法。

list = items.children()
print(type(list))
print(list)

# 如果要筛选所有子节点中符合条件的节点，比如我们想筛选出子节点中class为active的节点，可以向children()方法传入CSS选择器.active

list = items.children('.active')
print(list)


#2.2、父元素

#2.2.1、parent()
# 可以用parent()方法来获取某个节点的父节点

# 在这里我们首先用.list选取了class为list的节点，然后调用了parent()方法，得到其父节点，类型依然是PyQuery类型。
# 这里的父节点是该节点的直接父节点，也就是说，它不会再去查找父节点的父节点，即祖先节点。

doc = pq(html)
items = doc('.list')
container = items.parent()

print(type(container))
print(container)

#2.2.2、parents()
#如果我们想获取某个祖先节点怎么办呢？可以用parents()方法。

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''

doc = pq(html)
items = doc('.list')
parents = items.parents()
print(type(parents))
print(parents)

#parents查找所有的父亲节点,返回两个结果.

#parents可进行再次筛选
parent = items.parents('.wrap')
print(parent)


#2.3、兄弟元素

#2.3.1、siblings()
# 还有一种节点那就是兄弟节点，如果要获取兄弟节点可以使用siblings()方法。

# 属性没有加空格表表示同一个标签列里面,是并列的意思.在这里我们首先选择了class为list的节点内部的class为item-0和active的节点，也就是第三个li节点。
# 那么很明显它的兄弟节点有四个，那就是第一、二、四、五个li节点。可以看到运行结果也正是我们刚才所说的四个兄弟节点。

doc = pq(html)
li = doc('.list .item-0.active')
print(li.siblings())

# 在这里我们筛选了class为active的节点，通过刚才的结果我们可以观察到class为active的兄弟节点只有第四个li节点，所以结果应该是一个,
print(li.siblings('.active'))



#3、遍历


#3.1、单个元素
# 对于单个节点来说，我们可以直接打印输出，也可直接转成字符串。

doc = pq(html)
li = doc('.item-0.active')
print(li)


#3.2、多个元素

# 对于多个节点的结果，我们就需要遍历来获取了，例如这里我们把每一个li节点进行遍历,，需要调用items()方法。

# 在这里我们可以发现调用items()方法后，会得到一个生成器，遍历一下，就可以逐个得到li节点对象了，它的类型也是PyQuery类型。
# 所以每个li标签还可以调用前面所说的方法进行选择，比如继续查询子节点，寻找某个祖先节点等等，非常灵活。


doc = pq(html)
lis=doc("li").items()
print(type(list))

for li in lis:
    print(li)



#4、获取


#4.1、获取属性
# 提取到某个PyQuery类型的节点之后，我们可以调用attr()方法来获取属性,有两种方式可以进行获取,如下:

doc = pq(html)
a = doc('.item-0.active a')#这里有个空格,则选择里面的标签
print(a)

print(a.attr('href'))#方法一
print(a.attr.href)#方法二

#注意：
# 当返回结果包含多个节点时，调用attr()方法只会得到第一个节点的属性。
# 在进行属性获取的时候观察一下返回节点是一个还是多个，如果是多个，则需要遍历才能依次获取每个节点的属性。


#4.2、获取文本
# 获取节点之后的另一个主要的操作就是获取其内部的文本了，我们可以调用text()方法来获取

doc = pq(html)
a = doc('.item-0.active a')
print(a)

print(a.text())


#4.3、获取HTML
# 如果我们想要获取这个节点内部的HTML文本，就可以用html()方法。

doc = pq(html)
li = doc('.item-0.active')
print(li)

print(li.html())



#5、DOM操作


#5.1、addClass、removeClass
# 首先我们选中了第三个li节点，然后调用了removeClass()方法，将li的active这个class移除，后来又调用了addClass()方法，又将class添加回来。
# 每执行一次操作，就打印输出一下当前li节点的内容。

doc = pq(html)
li = doc('.item-0.active')
print(li)
# <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>

li.removeClass('active')  # [<li.item-0>]
print(li)
# <li class="item-0"><a href="link3.html"><span class="bold">third item</span></a></li>

li.addClass('active')  # [<li.item-0.active>]
print(li)
# <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>

# 可以看到一共进行了三次输出，第二次输出li标签的active这个class被移除了，第三次class又添加回来了。
# 所以说我们addClass()、removeClass()这些方法可以动态地改变节点的class属性。


#5.2、attr、css

#5.2.1、attr
# 当然除了操作class这个属性，也有attr()方法来专门针对属性进行操作
doc = pq(html)
li = doc('.item-0.active')
print(li)
# <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>

li.attr('name', 'link')  # [<li.item-0.active>]
print(li)
# <li class="item-0 active" name="link"><a href="link3.html"><span class="bold">third item</span></a></li>

# 在这里我们首先选中了li标签，然后调用attr()方法来修改/增加属性，第一个参数为属性名，第二个参数为属性值.如原来存在,则修改属性值,如不存在,则增加.

#5.2.2、css
#同理

doc = pq(html)
li = doc('.item-0.active')
print(li)
# <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>

li.css('font-size', '14px')#[<li.item-0.active>]
print(li)
# <li class="item-0 active" name="link" style="font-size: 14px"><a href="link3.html"><span class="bold">third item</span></a></li>


#5.3、remove
# remove顾名思义移除，remove()方法有时会为信息的提取带来非常大的便利。

html1 = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''

# 在这里有一段HTML文本，我们现在想提取Hello, World这个字符串，而不要p节点内部的字符串，这个怎样来提取？

doc = pq(html1)
wrap = doc('.wrap')
print(wrap.text())
# Hello, World
# This is a paragraph.

wrap.find('p').remove()#[<p>]
print(wrap.text())
# Hello, World

#注意:
# 在这里我们直接先尝试提取class为wrap的节点的内容，看看是不是我们想要的，运行结果是Hello, World,This is a paragraph.
# 然而这个结果还包含了内部的p节点的内容，也就是说text()把所有的纯文本全提取出来了。如果我们想去掉p节点内部的文本，可以选择再把p节点内的文本提取一遍，然后从整个结果中移除这个子串，但这个做法明显比较繁琐。
# 那这是remove()方法就可以派上用场了，我们可以接着这么做,我们首先选中了p节点，然后调用了remove()方法将其移除，然后这时wrap内部就只剩下Hello, World这句话了，然后再利用text()方法提取即可。
# 所以说，remove()方法可以删除某些冗余内容，来方便我们的提取。在适当的时候使用可以极大地提高效率。



#6、伪类选择器

# CSS选择器之所以强大，还有一个很重要的原因就是它支持多种多样的伪类选择器。
# 例如选择第一个节点、最后一个节点、奇偶数节点、包含某一文本的节点等等，我们用一个实例感受一下：

doc = pq(html)
li = doc('li:first-child')#节点、第一个
print(li)
li = doc('li:last-child')#节点、最后一个
print(li)
li = doc('li:nth-child(2)')#节点、第二个
print(li)
li = doc('li:gt(2)')#获取序号比2大的标签
print(li)
li = doc('li:nth-child(2n)')#获取偶数的标签,2n+1则是获得奇数
print(li)
li = doc('li:contains(second)')#包含second文本的
print(li)







