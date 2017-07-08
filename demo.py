class democls:
    def __init__(self):
        print("init")

    def demomethod1(self,a,b="b"):
        print(a,b)

    def demomethod2(url, data = None, headers = {}, origin_req_host = None, unverifiable = False, method = {}):
        print("url=",url, "\ndata=",data, "\nheaders=",headers,"\norigin_req_host=", origin_req_host, "\nunverifiable=",unverifiable , "\nmethod=",method )


d=democls
m=d.demomethod2("hah",{"header":"header"},"jj",method="m")#如果没有形参会按顺序赋值