import hashlib
import binascii
import time

from HttpRequest import HttpRequest
from conf import conf

class Authenticator:
    def authenticate(http_request):
        if not "TimeStamp" in http_request.headers:
            print("no timestamp")
            return False
            
        if not "Nonce" in http_request.headers:
            print("no nonce")
            return False
            
        if not "Signature" in http_request.headers:
            print("no sig")
            return False
            
        time_stamp = http_request.headers['TimeStamp']
        if(not Authenticator.is_valid(time_stamp)):
            print('nope')
            return False
        print('yeah')                  
        nonce = http_request.headers['Nonce']
        hash_string = str(nonce) + str(time_stamp) + str(conf.key)
        
        signature_client = "b'" + http_request.headers['Signature'] + "'"
        
        signature_server = str(binascii.hexlify(hashlib.sha256(hash_string).digest()))
        return signature_client == signature_server
    
    def is_valid(time_stamp):
        now = time.time()
        diff = abs(now - int(time_stamp))
        return diff < 5000

#foo = '''POST /relay HTTP/1.1\r\nHost: 192.168.22.139:8080\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\nTimeStamp: 1673391507\r\nSignature: 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b\r\nNonce: foobarmoep\r\nContent-Length: 18\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nstatus=Off&relay=1'''
#http = HttpRequest(foo)
#http.inspect()

#foo = Authenticator.authenticate(http)
#print (foo)