from HttpResponse import HttpResponse
import time

class Application:
    routes = [
        {'method':'GET',  'auth_required':False, 'path':'/', 			'action': 'default'},
        {'method':'GET',  'auth_required':False, 'path':'/status', 		'action': 'status'},
        {'method':'GET',  'auth_required':False, 'path':'/timestamp', 	'action': 'timestamp'},
        {'method':'GET',  'auth_required':False, 'path':'/relay', 		'action': 'changeStatusDisplay'},
        {'method':'POST', 'auth_required':True,  'path':'/relay', 		'action': 'changeStatus'}
    ]

    def __init__(self, relays):
        self.relays = relays

    def match(self, http_request):
        for route in self.routes:
            if((route['method'] == http_request.method) and (route['path'] == http_request.path)):
                print('matching...')
                return route['auth_required'], route['action']
        return False, "NotFound"

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
        
        if(action == 'changeStatusDisplay'):
            return self.changeStatusDisplay()
        
        if(action == 'changeStatus'):
           return self.changeStatus()
        
        return self.notFound()

#### actual application here #####################
    
    def default(self):
        response = HttpResponse("200", 'text/html', '<!DOCTYPE html>\n<html><body><h1>WiFi Relay</h1><p><ul><li><a href="/status">Current status</a></li><li><a href="/timestamp">Time Stamp</a></li><li><a href="https://github.com/misel228/wifi_relays">WiFi-Relay(Github project)</a></li></ul></p></body></html>')
        return response.render()

    def changeStatusDisplay(self):
        response = HttpResponse("200", 'text/html', '<!DOCTYPE html>\n<html><body><h1>WiFi Relay</h1><p>You need to POST here!</p></body></html>')
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
        response = HttpResponse("404", 'text/html', '<!DOCTYPE html>\n<html><body><h1>404</h1><p>Sorry, nothing here...</p></body></html>')
        return response.render()

    def AccessDenied(self):
        response = HttpResponse("403", 'text/html', '<!DOCTYPE html>\n<html><body><h1>403</h1><p>Access denied</p></body></html>')
        return response.render()

