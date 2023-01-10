import machine


class Relays:
    pins = None
    relays = None
    relay_status = [0,0,0,0]
    display = None

    def __init__(self, pins, display):
        print(pins)
        self.pins = pins
        self.display = display

        self.relays = [
            machine.Pin(pins[0], machine.Pin.OUT),
            machine.Pin(pins[1], machine.Pin.OUT),
            machine.Pin(pins[2], machine.Pin.OUT),
            machine.Pin(pins[3], machine.Pin.OUT)
        ]

        for relay in range(0,3):
            self.disable(relay)


    def enable(self, relay):
        print("turn on ")
        print(relay)
        self.relays[relay].value(1)
        self.relay_status[relay] = 1
        self.show_relay_status()
        
    def disable(self, relay):
        print("turn off ")
        print(relay)
        self.relays[relay].value(0)
        self.relay_status[relay] = 0
        self.show_relay_status()

    def show_relay_status(self):
        self.display.setRelayStatus(self.relay_status)
