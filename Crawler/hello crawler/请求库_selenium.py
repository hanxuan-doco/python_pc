# 什么是 selenium ？
# 其实它就是一个自动化测试工具，支持各种主流的浏览器


#0、这是一个selenium的实例，运行后可以发现会自动弹出一个浏览器，浏览器首先会跳转到百度，然后在搜索框中输入Python进行搜索，然后跳转到搜索结果页，等待搜索结果加载出来之后，控制台分别会输出当前的URL，当前的Cookies还有网页源代码。
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()   #定义使用谷歌浏览器
try:
    browser.get('https://www.baidu.com')  #访问百度
    input = browser.find_element_by_id('kw')  #定位百度网页输入框
    input.send_keys('Python')   #输入Python
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left'))) #查找
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()

#1、声明浏览器对象

browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.PhantomJS()
browser = webdriver.Safari()


#2、访问淘宝首页

browser = webdriver.Chrome()            #声明浏览器对象
browser.get('https://www.taobao.com')   #访问淘宝首页
print(browser.page_source)              #打印源码
browser.close()                         #关闭网页


#3、查找元素

#3.1、单个元素
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')
# 在这里我们使用了三种方式获取输入框，根据ID，CSS Selector，和XPath获取，它们返回的结果是完全一致的。
print(input_first, input_second, input_third)
browser.close()

#另外Selenium还提供了通用的find_element()方法，它需要传入两个参数，一个是查找的方式By，
# 另一个就是值，实际上它就是find_element_by_id()这种方法的通用函数版本，比如find_element_by_id(id)就等价于find_element(By.ID, id)。
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element(By.ID, 'q')
print(input_first)
browser.close()


#3.2、多个元素
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
print(type(lis))
browser.close()

#然后我们用find_elements来尝试一下
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
print(lis)
print(type(lis))
browser.close()


#4、元素交互

#输入文字用send_keys()方法，清空文字用clear()方法，另外还有按钮点击，用click()方法。

import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')  #定位输入框
input.send_keys('iPhone')                #输入iPhone
time.sleep(1)
input.clear()                            #清空文字
input.send_keys('iPad')                  #输入iPad
button = browser.find_element_by_class_name('btn-search') #定位标签
button.click()

#4.1、动作链

from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(source, target)
actions.perform()
# 首先我们打开网页中的一个拖拽实例，然后依次选中要被拖拽的元素和拖拽到的目标元素，
# 然后声明了ActionChains对象赋值为actions变量，然后通过调用actions变量的drag_and_drop()方法，然后再调用perform()方法执行动作，就完成了拖拽操作。

#4.2、执行JavaScript
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
#在这里我们就利用了execute_script()方法将进度条下拉到最底部，然后弹出alert提示框。


#5、获取元素信息

#5.1、获取属性
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
logo = browser.find_element_by_id('zh-top-link-logo')
print(logo)
print(logo.get_attribute('class'))

#5.2、获取文本值
browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.text)

#5.3、获取ID、位置、标签名、大小
browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)


#6.高阶用法

#6.1切换Frame
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
try:
    logo = browser.find_element_by_class_name('logo')
except NoSuchElementException:
    print('NO LOGO')
browser.switch_to.parent_frame()
logo = browser.find_element_by_class_name('logo')
print(logo)
print(logo.text)

#6.2、隐式等待
browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://www.zhihu.com/explore')
input = browser.find_element_by_class_name('zu-top-add-question')
print(input)

#6.3、显示等待
browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser, 10)
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
print(input, button)

#6.4、前进后退
import time

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')
browser.back()
time.sleep(1)
browser.forward()
browser.close()



#7、异常处理

from selenium.common.exceptions import TimeoutException, NoSuchElementException

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()