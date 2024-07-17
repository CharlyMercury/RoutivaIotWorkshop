from machine import ADC, Pin
import json


class DigitalPins:
    """
    This class controls actuators.

    Attributes:
        actuators (dict): Dictionary to store actuator pin objects keyed by location.
        actuators_list (list): List of actuators and their corresponding GPIO pins.
        actuators_list_locations (list): List of actuators locations.
    """
    def __init__(self, parameters, type_of_actuator):
        """
        Initializes a new instance of the Leds class.

        :param parameters: Dictionary containing LED configurations.
        """
        self.actuators = {}
        self.actuators_list = parameters[type_of_actuator]
        self.actuators_list_locations = []
        self.set_pins()

    def set_pins(self):
        """
        Sets the pins for LEDs and initializes them to off.
        """
        for actuator in self.actuators_list:
            pin_number, location = actuator
            self.actuators_list_locations.append(location)
            self.actuators[location] = Pin(pin_number, Pin.OUT)
            self.actuators[location].off()

    def write(self, location, state):
        """
        Turns the LED at the given location on or off based on the state.

        :param location: The location of the LED.
        :param state: True to turn on the LED, False to turn it off.
        """
        if location in self.actuators:
            if state:
                self.actuators[location].on()
            else:
                self.actuators[location].off()
        else:
            print(f"LED at location '{location}' not found.")


# Load parameters from file
with open(file='./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

# Initialize LEDs if the actuator type is 'leds'
if 'actuator' in parameters_:
    if parameters_['actuator'] == "leds":
        leds_iot = DigitalPins(parameters_, 'leds')
    if parameters_['actuator'] == "fans":
        leds_iot = DigitalPins(parameters_, 'fans')


def activate_actuator(actuator_name, location_, state_):
    """
    Activates or deactivates the specified actuator.

    :param actuator_name: The name of the actuator (e.g., 'leds').
    :param location_: The location of the actuator.
    :param state_: True to activate the actuator, False to deactivate it.
    """
    if actuator_name == "leds" and location_ in leds_iot.actuators_list_locations:
        leds_iot.write(location=location_, state=state_)
    if actuator_name == "fans" and location_ in leds_iot.actuators_list_locations:
        leds_iot.write(location=location_, state=state_)
    else:
        print(f"Actuator '{actuator_name}' at location '{location_}' not found or not supported.")
