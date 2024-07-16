"""

 To read ldr use
    - mosquitto_pub -d -t sensor -m '{"action": {"turn-on":"light", "state": true}}'
 to turn-off readings
    - mosquitto_pub -d -t sensor -m '{"action": {"turn-on":"light", "state": false}}'

 hearing reading
    -    mosquitto_sub -d -t sensors_value

 To turn-on a led use
    - mosquitto_pub -d -t actuator -m '{"action": {"turn-on":"leds", "location": "Comedor", "state": true}}'
 to turn-off a led
    - mosquitto_pub -d -t actuator -m '{"action": {"turn-on":"leds", "location": "Comedor", "state": false}}'

"""
import json
import time
import machine
import ubinascii
from umqttsimple import MQTTClient
import network
import esp
import gc
from read_sensor import read_sensor
from activate_actuator import activate_actuator

esp.osdebug(None)
gc.collect()

# Mqtt connection parameters
client_id_ = ubinascii.hexlify(machine.unique_id())

# Parameters File
with open(file=r'./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

# Global Variables
read_lights = False
activate_light = [False, {}]


def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print('Network Connection Successful')
    print(station.ifconfig())


def sub_cb(topic, msg):
    global read_lights, activate_light

    topic_str = topic.decode('utf-8')
    payload_message = json.loads(msg.decode('utf-8'))

    if topic_str == 'sensor':
        if 'turn-on' in payload_message['action']:
            if payload_message['action']['turn-on'] == parameters_['sensor']:
                if payload_message['action']['state']:
                    read_lights = True
                if not payload_message['action']['state']:
                    read_lights = False

    if topic_str == 'actuator':
        if 'turn-on' in payload_message['action'] and payload_message['action']['turn-on'] == parameters_['actuator']:
            activate_light = [True, payload_message]
        if 'turn-off' in payload_message['action'] and payload_message['action']['turn-off'] == parameters_['actuator']:
            activate_light = [False, payload_message]

    print(topic, msg, "read lights: ", read_lights, "activate_lights:", activate_light)


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


class LocalMqttClient:
    def __init__(self, endpoint, client_id, topics, parameters):
        self.endpoint = endpoint
        self.client_id = client_id
        self.topics = topics
        self.parameters = parameters

        # Create a Mqtt Connection
        self.client = MQTTClient(self.client_id, self.endpoint)
        self.client.set_callback(sub_cb)
        self.client.connect()
        print(f'Connected to MQTT broker: {endpoint}')

    def subscribe_to_topics(self):
        for topic in self.topics:
            topic_sub = topic.encode()
            self.client.subscribe(topic=topic_sub, qos=1)
            print(f"Subscribe to {topic}")

    def publish_to_topics(self, topic: str, input_message: dict):
        if input_message:
            message_json = json.dumps(input_message)
            topic_pub = topic[0].encode()
            message_json_byte = message_json.encode()
            self.client.publish(topic=topic_pub, msg=message_json_byte, qos=1)

    def check_msg(self):
        self.client.check_msg()


ssid_ = parameters_["ssid"]
password_ = parameters_["password"]
connect_wifi(ssid=ssid_, password=password_)

client = None
try:
    client = LocalMqttClient(
        endpoint=parameters_["endpoint"],
        client_id=client_id_,
        topics=parameters_["sub_topics"],
        parameters=parameters_)
    client.subscribe_to_topics()
except OSError as err:
    print(err)
    restart_and_reconnect()

while True:

    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()

    if read_lights:
        value = read_sensor(parameters_['sensor'])
        client.publish_to_topics(topic=parameters_["pub_topics"], input_message=value)
        time.sleep(0.9)

    if activate_light[0] and 'action' in activate_light[1]:
        value = activate_actuator(activate_light[1]['action']['turn-on'],
                                  activate_light[1]['action']['location'],
                                  activate_light[1]['action']['state'])
        activate_light[1] = {}

    if not activate_light[0] and 'action' in activate_light[1]:
        value = activate_actuator(activate_light[1]['action']['turn-off'],
                                  activate_light[1]['action']['location'],
                                  activate_light[1]['action']['state'])
        activate_light[1] = {}

    time.sleep(0.5)
