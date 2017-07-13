import re
import urllib.request

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




def link_crawer(seed_url,link_regex):
    '''crawl from the given seef URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    #keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        #filter for links matching our regex expression
        for link in get_links(html):
            #check ig link matches expectes regex
            if re.match(link_regex,link):
                #form absolute link
                link = urllib.urlparse.urljoin(seed_url,link)
                #check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def get_links(html):
    '''return a list of links from html
    '''
    # a regular expression to extract all links the webpage
    webpage_regex = re.compile('<[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    #html = html.decode('utf-8')
    return webpage_regex.findall(html)

link_crawer('http://example.webscraping.com','/(index|view)')