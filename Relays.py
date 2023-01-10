import machine


class Relays:
    pins = None
    relays = None
    relay_status = [0,0,0,0]
    display = None

    def __init__(self, pins, display):
        self.pins = pins
        self.display = display

        self.relays = [
            machine.Pin(pins[0], machine.Pin.OUT),
            machine.Pin(pins[1], machine.Pin.OUT),
            machine.Pin(pins[2], machine.Pin.OUT),
            machine.Pin(pins[3], machine.Pin.OUT)
        ]

        for relay in range(0,4):
            print(relay)
            self.disable(relay)


    def enable(self, relay):
        print("turn on ")
        print(relay)
        if(self.relay_boundary_check(relay)):
            self.relays[relay].value(1)
            self.relay_status[relay] = 1
            self.show_relay_status()
        
    def disable(self, relay):
        print("turn off ")
        print(relay)
        if(self.relay_boundary_check(relay)):
            self.relays[relay].value(0)
            self.relay_status[relay] = 0
            self.show_relay_status()

    def show_relay_status(self):
        self.display.setRelayStatus(self.relay_status)
    
    def relay_boundary_check(self, relay):
        if(relay < 0):
            return False
        if(relay > 3):
            return False
        return True

#from display import Display
#display = Display(True)
#relays = Relays([2,3,15,13],display)