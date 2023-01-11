class HttpRequest:

    method = 'GET'
    path = ''
    headers = {}
    body = {}

    def __init__(self, http_data):
        self.parseHttpRequest(http_data)
    
    def inspect(self):
        print('method')
        print(self.method)
        print('path')
        print(self.path)
        print('headers')
        print(self.headers)
        print('body')
        print(self.body)

    def splitHttpRequest(self, http_data):
        split_at = http_data.find("\r\n\r\n")
        headers = http_data[0:split_at].split("\r\n")
        body = http_data[(split_at+4):]
        return headers,body;
        
    def parseHttpHeader(self, headers):
        foo = headers[0].find(" ")
        self.method = headers[0][0:foo]

        foo2 = headers[0].find(" ", foo + 1)
        self.path = headers[0][foo+1:foo2]

        del(headers[0])
    
        h = dict()
        for header in headers:
            foo = header.find(": ")
            key = header[0:foo]
            value = header[foo+2:]
            h[key] = value

        self.headers = h

    def parseHttpBody(self, body):
        params = body.split('&')

        p = dict()
        for param in params:
            foo = param.find("=")
            key = param[0:foo]
            value = param[foo+1:]
            p[key] = value

        return p

    def parseHttpRequest(self, http_data):
        headers,body = self.splitHttpRequest(http_data)

        self.parseHttpHeader(headers)
        self.body = self.parseHttpBody(body)

    def params(self):
        return self.body

#foo = '''GET /status HTTP/1.1\r\nHost: 192.168.22.139:8080\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n'''
#http = HttpRequest(foo)
#http.inspect()
    