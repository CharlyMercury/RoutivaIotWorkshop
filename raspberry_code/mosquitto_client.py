import sys
import threading
from paho.mqtt import client as mqtt_client


class MosquittoClient(threading.Thread):
    def __init__(self, broker_address, message_queue, parameters):
        threading.Thread.__init__(self)
        self.parameters = parameters
        self.topics = parameters['topics_to_subscribe_mosquitto']
        self.broker_address = broker_address
        self.port = 1883
        self.message_queue = message_queue
        self.client = mqtt_client.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self._stop = threading.Event()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to Mosquitto with result code " + str(rc))
        print(f"Mosquitto Client subscribed to topics: {self.topics}")
        for topic_sub in self.topics:
            self.client.subscribe(topic_sub)
            # print("Subscribed with {}".format(str(subscribe_result['qos'])))

    def on_message(self, client, userdata, msg):
        # print(f"Received message from Mosquitto: {msg.topic} {msg.payload}")
        # Put the message in the queue
        self.message_queue.put(("mosquitto", msg.topic, msg.payload))

    def run(self):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_forever()
        while True:
            pass
