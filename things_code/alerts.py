from machine import Pin
from time import sleep
import json

motion = False

def handle_interrupt(pin):
  global motion
  motion = True
  global interrupt_pin
  interrupt_pin = pin 


# Load parameters from file
with open(file='./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

# Initialize alerts if the actuator type is 'alerts'
if 'sensor' in parameters_:
    if parameters_['sensor'] == "alerts":
        pir = Pin(14, Pin.IN)
        pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

def alert_interrup(motion_new_value):
    global motion
    if not motion_new_value:
        motion = False
    return motion
