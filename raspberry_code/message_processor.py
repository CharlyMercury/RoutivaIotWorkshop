import threading
import json


class MessageProcessor(threading.Thread):
    def __init__(self, message_queue, mosquitto_client_instance, aws_client_instance):
        threading.Thread.__init__(self)
        self.message_queue = message_queue
        self.mosquitto_client_instance = mosquitto_client_instance
        self.aws_client_instance = aws_client_instance

    def run(self):
        while True:
            source, topic, payload = self.message_queue.get()
            if source == "mosquitto":
                print(f"Forwarding message from Mosquitto to AWS: {topic} {payload}")
                self.aws_client_instance.publish_to_topics(topic, json.loads(payload))
            elif source == "aws":
                print(f"Forwarding message from AWS to Mosquitto: {topic} {payload}")
                self.mosquitto_client_instance.client.publish(topic, payload)
            if topic == 'exit':
                exit(0)
