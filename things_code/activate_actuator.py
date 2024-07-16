from machine import ADC, Pin
import json


class Leds:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, parameters):
        """
        Initializes a new instance.
        parameter pin A pin that's connected to an LDR.
        """

        # initialize ADC (analog to digital conversion)
        self.leds = {}
        self.leds_list = parameters['leds']
        self.set_pins()

    def set_pins(self):

        for led in self.leds_list:
            self.leds[led[1]] = Pin(led[0], Pin.OUT)
            self.leds[led[1]].off()

    def write(self, location, state):
        if state:
            print(location, state, dir(self.leds[location]))
            self.leds[location].on()
        if not state:
            print(location, state)
            self.leds[location].off()


# Parameters File
with open(file=r'./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

if 'actuator' in parameters_ and parameters_['actuator'] == "leds":
    # initialize a Led
    leds_iot = Leds(parameters_)


def activate_actuator(actuator_name, location_, state_):

    if actuator_name == "leds":
        leds_iot.write(location=location_, state=state_)
