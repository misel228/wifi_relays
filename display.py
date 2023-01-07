from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import utime,time


class Display:
    WIDTH  = 128
    HEIGHT = 32
    oled = None

    ip_address = ''
    relay_status = [0,0,0,0]

    ########  Function to init OLED ####################
    def __init__(self):
        print("init i2c")
        i2c = I2C(1,freq=200000,sda=Pin(6),scl=Pin(7))
        print(i2c)
        print("I2C Address  : "+hex(i2c.scan()[0]).upper()) # Display device address
        print("I2C Configuration: "+str(i2c))
        print("+++++++++++++++++++++")

        self.oled = SSD1306_I2C(self.WIDTH, self.HEIGHT, i2c)                  # Init oled display
        
        self.flash("INIT", 1)

    def setIp(self, ip_address):
        self.ip_address = ip_address
        self.refresh()

    def setRelayStatus(self, relay_status):
        self.relay_status = relay_status
        self.refresh()

    def refresh(self):
        self.displayRelayStatus()
        self.displayIp()

    def displayIp(self):
        self.oled.text(self.ip_address,10,20)
        self.oled.show()

    def displayRelayStatus(self):
        self.oled.fill(0)
        status_string = ""
        for relay in range(0,4):
            status_string = status_string + " " + str(self.relay_status[relay])
        self.oled.text(status_string,5,5)
        self.oled.show()

    def flash(self, text, duration = 1):
        self.oled.fill(0)
        self.oled.text(text,5,5)
        self.oled.show()
        time.sleep(duration)
        self.refresh()
