import re
import  demo3downloadwebpage

def link_crawer(seed_url,link_regex):
    '''crawl from the given seef URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = demo3downloadwebpage.download(url)
        #filter for links matching our regex expression
        for link in get_links(html):
            if re.match(link_regex,link):
                crawl_queue.append(link)

def get_links(html):
    '''return a list of links from html
    '''
    # a regular expression to extract all links the webpage
    webpage_regex = re.compile('<a<^>>+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    #html = html.decode('utf-8')
    return webpage_regex.findall(html)

link_crawer('http://example.webscraping.com','/(index|view)')