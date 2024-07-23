"""
Instructions:
 To read LDR use:
    - mosquitto_pub -d -t sensor -m '{"action": {"turn-on":"light", "state": true}}'
 To turn off readings:
    - mosquitto_pub -d -t sensor -m '{"action": {"turn-on":"light", "state": false}}'
 To hear readings:
    - mosquitto_sub -d -t sensors_value

 To turn on a LED use:
    - mosquitto_pub -d -t actuator -m '{"action": {"turn-on":"leds", "location": "sala", "state": true}}'
 To turn off a LED:
    - mosquitto_pub -d -t actuator -m '{"action": {"turn-on":"leds", "location": "sala", "state": false}}'

    "leds": [[4, "comedor"], [5, "sala"], [19, "dormitorio"], [21, "descanso"], [25, "azotea"],
    [26, "jardin"], [27, "exterior"]]

 To turn on a fan use:
    - mosquitto_pub -d -t actuator -m '{"action": {"turn-on":"fans", "location": "cocina", "state": true}}'
 To turn off a fan:
    - mosquitto_pub -d -t actuator -m '{"action": {"turn-on":"fans", "location": "cocina", "state": false}}'
    "fans": [[4, "cocina"]]

"""

import json
import time
import machine
import ubinascii
import network
import esp
import gc
from umqttsimple import MQTTClient
from read_sensor import read_sensor
from activate_actuator import activate_actuator
from alerts import alert_interrup

# Disable OS debugging and collect garbage
esp.osdebug(None)
gc.collect()

# MQTT connection parameters
client_id_ = ubinascii.hexlify(machine.unique_id())

# Load parameters from file
with open(file='./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

# Global variables
read_sensors = False
activate_actuator_var = [False, {}]


def connect_wifi(ssid, password):
    """
    Connect to the Wi-Fi network.

    :param ssid: Wi-Fi SSID
    :param password: Wi-Fi password
    """
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print('Network Connection Successful')
    print(station.ifconfig())


def sub_cb(topic, msg):
    """
    MQTT subscription callback function.

    :param topic: The topic of message
    :param msg: The message payload
    """
    global read_sensors, activate_actuator_var
    topic_str = topic.decode('utf-8')
    payload_message = json.loads(msg.decode('utf-8'))

    print(payload_message)

    if topic_str == 'sensor':
        if 'turn-on' in payload_message['action'] and payload_message['action']['turn-on'] == parameters_['sensor']:
            read_sensors = payload_message['action']['state']

    if topic_str == 'actuator':
        action_ = payload_message['action']
        if 'turn-on' in action_ and action_['turn-on'] == parameters_['actuator']:
            activate_actuator_var = [True, payload_message]
        elif 'turn-off' in action_ and action_['turn-off'] == parameters_['actuator']:
            activate_actuator_var = [False, payload_message]


def restart_and_reconnect():
    """
    Restart and reconnect to the MQTT broker.
    """
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


class LocalMqttClient:
    """
    Local MQTT client class to manage MQTT operations.
    """
    def __init__(self, endpoint, client_id, topics, parameters):
        """
        Initialize the LocalMqttClient instance.

        :param endpoint: MQTT broker endpoint
        :param client_id: Client ID
        :param topics: List of topics to subscribe to
        :param parameters: Configuration parameters
        """
        self.endpoint = endpoint
        self.client_id = client_id
        self.topics = topics
        self.parameters = parameters

        # Create MQTT connection
        self.client = MQTTClient(self.client_id, self.endpoint)
        self.client.set_callback(sub_cb)
        self.client.connect()
        print(f'Connected to MQTT broker: {endpoint}')

    def subscribe_to_topics(self):
        """
        Subscribe to the specified topics.
        """
        for topic in self.topics:
            self.client.subscribe(topic.encode(), qos=1)
            print(f"Subscribed to {topic}")

    def publish_to_topics(self, topic: str, input_message: dict):
        """
        Publish a message to a specified topic.

        :param topic: Topic to publish to
        :param input_message: Message payload as a dictionary
        """
        if input_message:
            message_json = json.dumps(input_message).encode()
            print(topic, message_json)
            self.client.publish(topic.encode(), msg=message_json, qos=1)

    def check_msg(self):
        """
        Check for new messages.
        """
        self.client.check_msg()


# Connect to Wi-Fi
ssid_ = parameters_["ssid"]
password_ = parameters_["password"]
connect_wifi(ssid=ssid_, password=password_)


# Initialize and connect MQTT client
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


# Main loop
while True:
    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()

    if read_sensors:
        value = read_sensor(parameters_['sensor'])
        client.publish_to_topics(topic=parameters_["pub_topics"], input_message=value)
        time.sleep(1)

    if activate_actuator_var[0] and 'action' in activate_actuator_var[1]:
        action = activate_actuator_var[1]['action']
        value = activate_actuator(action['turn-on'], action['location'], action['state'])
        activate_actuator_var[1] = {}

    if not activate_actuator_var[0] and 'action' in activate_actuator_var[1]:
        action = activate_actuator_var[1]['action']
        value = activate_actuator(action['turn-off'], action['location'], action['state'])
        activate_actuator_var[1] = {}

    if 'sensor' in parameters_:
        if parameters_['sensor'] == "alerts":
            motion = alert_interrup(True)
            if motion == True:
                value = {"alerta": "Movimiento detectado"}
                print(parameters_["pub_topics"], value)
                client.publish_to_topics(topic=parameters_["pub_topics"][0], input_message=value)
                time.sleep(5)
                motion = alert_interrup(False)

    time.sleep(0.1)
