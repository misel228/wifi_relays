from machine import UART, Pin,SPI,I2C
import utime,time


from HttpRequest import HttpRequest
from Relays import Relays
from display import Display
from conf import conf
from esp import esp
from actions import Actions
from application import Application

display = Display(conf.use_oled_dummy)

esp = esp()
print("init wifi")
esp.initWifi(conf.ssid, conf.pwd)

print("init Server")
ip = esp.initServer(conf.Port)

if(ip != None):
    print(ip)
    display.setIp(ip)

    relays = Relays(conf.relay_pins, display)

    while True:
        Connection_ID,data=esp.ReceiveData()
        if(Connection_ID != None):
            request = HttpRequest(data)
            application = Application(relays)
            foo,action = application.match(request)
            print(action)
            http_response = application.execute(action, request.params)
            
            esp.sendData(Connection_ID,http_response)

