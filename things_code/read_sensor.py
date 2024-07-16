from machine import ADC, Pin
import json


class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, description: str = 'None'):
        """
        Initializes a new instance.
        parameter pin A pin that's connected to an LDR.
        """

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))
        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)
        self.description = description

    def read(self):
        """
        Read a raw value from the LDR.
        return A value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        return a value and description.
        """
        return self.read() / 4095, self.description


# Parameters File
with open(file=r'./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

if 'sensor' in parameters_ and parameters_['sensor'] == "light":
    # initialize an LDR
    print(parameters_['ldr'][0][0], parameters_['ldr'][0][1])
    print(parameters_['ldr'][1][0], parameters_['ldr'][1][1])
    ldr_1 = LDR(parameters_['ldr'][0][0], parameters_['ldr'][0][1])
    ldr_2 = LDR(parameters_['ldr'][1][0], parameters_['ldr'][1][1])


def read_sensor(sensor_name: str):

    if sensor_name == "light":
        value = ldr_1.value()
        value2 = ldr_2.value()
        return {"value": [value, value2]}
