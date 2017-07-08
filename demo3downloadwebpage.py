import urllib.request

def download(url , user_agent = "wswp" , num_retries=2):
    print("downloading ",url)
    headers = {"user-agent":user_agent}
    urllib.request.Request(url,headers=headers)
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.request.URLError as  e:
        print("download error:",e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e,"code") and 500 <= e.code <600:
                return download(url,num_retries-1)
    return html

download("http://baidu.com")
#download("http://httpstat.us/500")
#download("http://www.meetup.com")