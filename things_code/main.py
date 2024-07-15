import json
import time
import machine
from machine import Pin, ADC
import ubinascii
from umqttsimple import MQTTClient

# Mqtt connection parameters
client_id_ = ubinascii.hexlify(machine.unique_id())
mqtt_local_broker = '192.168.0.22'
subscribe_topics = [b'']


def sub_cb(topic, msg):
    payload_message = json.loads(msg.decode('utf-8'))
    print(topic, payload_message)


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
        for topic_sub in self.topics:
            # client.subscribe(b'machine_status/smoke_extractor')
            self.client.subscribe(topic=topic_sub, qos=1)

    def publish_to_topics(self, topic_pub: str, input_meesage: dict):
        if input_meesage:
            message_json = json.dumps(input_meesage)
            self.client.publish(topic=topic_pub, msg=message_json, qos=1)

    def check_msg(self):
        self.client.check_msg()


client = None
try:
    client = LocalMqttClient(endpoint=mqtt_local_broker, client_id=client_id_, topics=subscribe_topics)
except OSError as err:
    print(err)
    restart_and_reconnect()


while True:

    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()

    time.sleep(0.5)
