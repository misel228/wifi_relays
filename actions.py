class Actions:
    routes = [
        {'method':'GET', 'path':'/', 'action': 'default'},
        {'method':'GET', 'path':'/status', 'action': 'status'},
        {'method':'POST', 'path':'/relay', 'action': 'changeStatus'}
    ]
    
    def match(self, http_request):
        for route in self.routes:
            if((route['method'] == http_request.method) and (route['path'] == http_request.path)):
                print('matching...')
                return route['action']