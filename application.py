from HttpResponse import HttpResponse
import time

class Application:
    routes = [
        {'method':'GET', 'path':'/', 'action': 'default'},
        {'method':'GET', 'path':'/status', 'action': 'status'},
        {'method':'GET', 'path':'/timestamp', 'action': 'timestamp'},
        {'method':'POST', 'path':'/relay', 'action': 'changeStatus'}
    ]

    def __init__(self, relays):
        self.relays = relays

    def match(self, http_request):
        for route in self.routes:
            if((route['method'] == http_request.method) and (route['path'] == http_request.path)):
                print('matching...')
                return route['action']

    params = []
    action = ''

    def execute(self, action, params):
        print('executing')
        print(action)

        self.params = params
        if(action == 'default'):
            return self.default()
        
        if(action == 'status'):
            return self.status()
        
        if(action == 'timestamp'):
            return self.timestamp()
        
        if(action == 'changeStatus'):
            return self.changeStatus()
        
        return self.notFound()

#### actual application here #####################
    
    def default(self):
        print('executing default action')
        response = HttpResponse("200", 'text/html', 'foobarmoep')
        return response.render()

    def changeStatus(self):
        params = self.params()
        relay = int(params['relay'])
        if(params['status']=='On'):
            self.relays.enable(relay)
            response = HttpResponse("200", 'text/plain', 'On')
            return response.render()
        else:
            self.relays.disable(relay)
            response = HttpResponse("200", 'text/plain', 'Off')
            return response.render()

    def status(self):
        status_string = '{'
        for relay in range(0,4):
            status_string = status_string  + ' "' + str(relay) + '" : ' + str(self.relays.relay_status[relay])
            if(relay < 3):
                status_string = status_string + ", "
        status_string = status_string + '}'
        response = HttpResponse("200", 'application/json', status_string)
        return response.render()
    
    def timestamp(self):
        response = HttpResponse("200", 'text/plain', str(time.time()))
        return response.render()
    
    def notFound(self):
        response = HttpResponse("404", 'text/plain', '404')
        return response.render()
