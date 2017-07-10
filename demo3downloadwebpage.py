import urllib.request
import re

def download(url , user_agent = "wswp" , num_retries=2):
    print("downloading : ",url)
    headers = {"user-agent":user_agent}
    urllib.request.Request(url,headers=headers)
    try:
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')     #python2和3兼容问题
    except urllib.request.URLError as  e:
        print("download error:",e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e,"code") and 500 <= e.code <600:
                return download(url,num_retries-1)
    return html

def crawl_sitemap(url):
    #dwonload the sitemap file
    sitemap = download(url)
    #extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    #downlod each lin
    for link in links:
        html = download(link)

crawl_sitemap("http://localhost:8080/pydemo/sitemap.xml")


#download("http://baidu.com")
#download("http://httpstat.us/500")
#download("http://www.meetup.com")