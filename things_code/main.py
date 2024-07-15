import json
import time
import machine
import ubinascii
from umqttsimple import MQTTClient
import network
import esp
import gc
from read_sensor import read_sensor_

esp.osdebug(None)
gc.collect()

# Mqtt connection parameters
client_id_ = ubinascii.hexlify(machine.unique_id())

# Parameters File
with open(file=r'./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters_ = json.load(file)

# Global Variables
activate_light = False


def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print('Network Connection Successful')
    print(station.ifconfig())


def sub_cb(topic, msg):
    global activate_light

    topic_str = topic.decode('utf-8')
    payload_message = json.loads(msg.decode('utf-8'))

    if topic_str == 'sensor':
        if 'turn-on' in payload_message['action']:
            if payload_message['action']['turn-on'] == parameters_['sensor']:
                if payload_message['action']['state']:
                    activate_light = True
                if not payload_message['action']['state']:
                    activate_light = False

    print(topic, msg, activate_light)


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

    if activate_light:
        value = read_sensor_(parameters_['sensor'])
        client.publish_to_topics(topic=parameters_["pub_topics"], input_message=value)
        time.sleep(0.9)

    time.sleep(0.1)
