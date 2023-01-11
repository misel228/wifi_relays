from machine import Pin, I2C, UART, ADC
import utime
import time
from ssd1306 import SSD1306_I2C # save this library in PiSquare


def enable(relay):
    print("turn on ")
    print(relay)
    relays[relay].value(1)
    relay_status[relay] = 1
    show_relay_status()
    
def disable(relay):
    print("turn off ")
    print(relay)
    relays[relay].value(0)
    relay_status[relay] = 0
    show_relay_status()

def show_relay_status():
    oled.fill(0)
    status_string = ""
    for relay in range(0,4):
        status_string = status_string + " " + str(relay_status[relay])
    oled.text(status_string,5,5)
    oled.show()    

WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height

i2c = I2C(1,freq=200000,sda=Pin(6),scl=Pin(7))
print(i2c)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)

oled.fill(0)
oled.text("SB COMPONENTS",10,5)
oled.text("PiSquare",30,25)
oled.show()

relays = [
    machine.Pin(2, machine.Pin.OUT),
    machine.Pin(3, machine.Pin.OUT),
    machine.Pin(15, machine.Pin.OUT),
    machine.Pin(13, machine.Pin.OUT)
]

relay_status = [
    0,0,0,0
]

for relay in range(0,4):
    disable(relay)


time.sleep(1)

while 1:
    for relay in range(0,4):
        enable(relay)
        time.sleep(1)
    
    
    for relay in range(0,4):
        disable(relay)
        time.sleep(1)    
    
    reading = sensor_temp.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = round(27 - (reading - 0.706)/0.001721,2)
    print(temperature)
    oled.fill(0)
    oled.text(str(temperature),30,25)
    oled.show()
    break

enable(2)
time.sleep(1)    

enable(3)
time.sleep(1)    

disable(2)
time.sleep(1)    

disable(3)
time.sleep(1)    


