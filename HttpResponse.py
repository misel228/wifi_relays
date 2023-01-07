class HttpResponse:
    def __init__(self, response_code, mime_type, body):
        self.response_code = response_code
        self.mime_type = mime_type
        self.body = body

    def render(self):
        response = 'HTTP/1.1 '
        response = response + self.response_code
        response = response + '\r\n'
        response = response + 'Content-Type: ' + self.mime_type + '\r\n\r\n'
        response = response + self.body
        return response