from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError
from pyquery import pyquery as pq


base_url = "http://weixin.sogou.com/weixin?"
keyword = "风景"
proxy_pool_url = "http://127.0.0.1:6379/get"
proxy = None
headers = {
    'Cookie':'SUV=00B1326AB7C630315C0CFE21A67ED079; SMYUV=1544358775226378; ssuid=6704913197; CXID=780AE680BE91D9A103B7D57F167EB0F5; pgv_pvi=7787655168; sg_uuid=1556519617; MTRAN_ABTEST=1; ad=k6x5vZllll2t08w8lllllVhzMIZlllllTHfFSyllllGlllllph7ll5@@@@@@@@@@; SUID=4993DEDE3108990A000000005C0E5482; IPLOC=CN1306; YYID=16CF2FB8163645214032616DC3248E05; cd=1554711416&16de143ba76548415d0485b679365589; ld=GZllllllll2tROvjg37RWVhrjyHt$Z2cTHfFvyllllYllllxjllll5@@@@@@@@@@; LSTMV=207%2C182; LCLKINT=5124; UM_distinctid=16a0ef648cb40-00f374501438cd-4d045769-100200-16a0ef648cc31b; toutiao_city_news=%E5%8C%97%E4%BA%AC; _ga=GA1.2.2014798730.1548071152; SNUID=3EE5A8A97773F0F01C8F7EC0774D1941; ABTEST=0|1555294406|v1; weixinIndexVisited=1; sct=21; td_cookie=442154158; ppinf=5|1555399219|1556608819|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlQUYlOTIlRTYlOUElODR8Y3J0OjEwOjE1NTUzOTkyMTl8cmVmbmljazoxODolRTUlQUYlOTIlRTYlOUElODR8dXNlcmlkOjQ0Om85dDJsdUNnQXFZX0FtTFplMnJMNTUteUxZT1lAd2VpeGluLnNvaHUuY29tfA; pprdig=ulxNHWR4jvpaEY2tj2mjCS9oZKCwY63MruXNMizlfT399Hiul-ncZXlswQeyJkIvlqPYl99nX0os32n-crP44F2xGQrX1FhNruo_1yokcFe3-zLAbnWyNiK4qdsbvZkZ2Cmp26CnNRVlb6dd4P_gdxc4inL4b0ybF3bGPQImWag; sgid=17-40098953-AVy1gjOmVCguYUHpA8zJXu4; usid=tOhDXIj3ncZIS1-M; ppmdig=15554007780000007a5d832dea52463ca88efd258eca4c76; JSESSIONID=aaa2uWETmzNsn7Avs_KOw',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}
max_count = 5


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        print("proxy_pool_url",proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except  ConnectionError:
        return None

def get_html(url,count=1):
    print("dizhi:",url)
    print("cishu",count)
    global proxy
    if count >= max_count:
        print("Tried Too Many Counts")
        return None
    try:
        if proxy:
            proxies = {
                'http':'http://'+proxy
            }
            response = requests.get(url,allow_redirects = False, headers=headers,proxies=proxies)
        else:
            response = requests.get(url,allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print("302")
            proxy = get_proxy()
            if proxy:
                print("Using proxy",proxy)
                return get_html(url)
            else:
                print("Get proxy Failed")
                return None
    except ConnectionError as e:
        print("Error Occueed",e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url,count)

def get_index(keyword,page):
    data = {
        'query': keyword,
        'type':2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return  html

# def paese_index(html):
#     doc = pq(html)
#     items = doc('.news-box .news-list li .txt-box h3 a').items()
#     for item in items:
#         yield item.attr('href')


def main():
    for page in range(1,101):
        html = get_index(keyword,page)
        print("main",html)
        # if html:
        #     aeticle_urls = paese_index(html)
        #     for aeticle_url in aeticle_urls:
        #         print(aeticle_url)

if __name__ == "__main__":
    main()


