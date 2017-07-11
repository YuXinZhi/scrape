import urllib.request
import re
import urllib.parse
import urllib.robotparser
import datetime
import time

import random


def download(url, user_agent="wswp", proxy=None, num_retries=2):
    print("downloading : ", url)
    headers = {"user-agent": user_agent}
    urllib.request.Request(url, headers=headers)

    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')  # python2和3兼容问题
    except urllib.request.URLError as  e:
        print("download error:", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, "code") and 500 <= e.code < 600:
                # retry 5xx HTTP errors
                return download(url, user_agent, proxy, num_retries - 1)
    return html

def crawl_sitemap(url):
    #dwonload the sitemap file
    sitemap = download(url)
    #extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    #downlod each lin
    for link in links:
        html = download(link)

class Throttle:
    '''add a delay between downloads for each domain
    '''
    def __init__(self,delay):
        #amout of delay between downloads for each domain
        self.delay = delay
        #timestamp of when a domain was last accessed
        self.domains = {}
    def wait(self,url):
        domain = urllib.request.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                #domain has been accessed recently so need to sleep
                time.sleep(sleep_secs)
        #update the last accessed time
        self.domains[domain] = datetime.datetime.now()




#crawl_sitemap("http://localhost:8080/pydemo/sitemap.xml")

#download("http://baidu.com")
#download("http://httpstat.us/500")
#download("http://www.meetup.com")

'''
import itertools
#maxmum number of consecutive download errors allowed
max_errors = 5
#current number of consecutive download errors allowed
num_errors = 0

for page in itertools.count(1):
    url = "http://example.webscraping.com/view/-%d"%page
    html = download(url)
    if html is None:
        #receive an error trying to download this webpage
        num_errors+=1
        if num_errors == max_errors:
            #reached maximum number of consecutive errors so exit
            break
    else:
        #success - can scrap the result
        num_errors = 0
        pass
'''


def link_crawler(seed_url,link_regex,max_depth=2):

    '''crawl from the given seef URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    max_depth = 2
    #keep track which URL's have seen before
    seen = set(crawl_queue)
    depth = seen[seed_url]
    rp=urllib.robotparser.RobotFileParser()
    rp.set_url(seed_url+"/robots.txt")
    rp.read()
    url = "http://example.webscraping.com"
    user_agent = "BadCrawler"
    while crawl_queue:
        url = crawl_queue.pop()
        #check url passes robots.txt restrictions
        if rp.can_fetch(user_agent,url):
            html = download(url)
            #filter for links matching our regular expression
            for link in get_links(html):
                #check if link matches expected regex
                if re.match(link_regex,link):
                    #form absulute link
                    link = urllib.parse.urljoin(seed_url,link)
                    #check if have already seen this link
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
        else:
            print("blocked by robots.txt",url)

def get_links(html):
    '''return a list of links from html
    '''
    #a regular expression to extract all links the webpage
    webpage_regex = re.compile('<a<^>>+href=["\'](.*?)["\']',re.IGNORECASE)
    #list of all links from the webpage
    return webpage_regex.findall(html)


class Downloader:
    def __init__(self,delay=5,user_agent="wswp",proxies=None,num_retries=1,cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self,url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                if self.num_retries > 0 and 500 <= result["code"] < 600:
                    #server eeror so ignore result from cache so still need download
                    result = None
        if result is None:
            #result was not loaded from cache so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {"User-agent":self.user_agent}
            result = self.download(url,headers,proxy,self.num_retries)
            if self.cache:
                #save result to cache
                self.cache[url] = result
        return result["html"]

