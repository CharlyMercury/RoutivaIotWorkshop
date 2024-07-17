# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
import os
import json
import queue
from mosquitto_client import MosquittoClient
from aws_client import AwsMqttClient
from message_processor import MessageProcessor

message_queue = queue.Queue()
# Get the current working directory
current_path = os.getcwd()
file_path_src = os.path.join(current_path, 'src')
file_path_certificates = os.path.join(file_path_src, 'certificates')

with open(file=r'./parameters_configuration.json', mode='r', encoding='utf-8') as file:
    parameters = json.load(file)

endpoint = parameters["endpoint"]
port = 443
cert = r"./certificates/certificado.cert.pem"
key = r"./certificates/certificado.private.key"
ca = r"./certificates/root-CA.crt"
client_id = parameters["client"]
topics_aws_subs = parameters["topics_to_subscribe_aws"]
topics_aws_pubs = parameters["topics_to_publish_aws"][0]

mosquitto_client_instance = MosquittoClient("192.168.1.101", message_queue, parameters)
aws_client_instance = AwsMqttClient(endpoint, port, cert, key, ca, client_id, topics_aws_subs, parameters, message_queue)
message_processor_instance = MessageProcessor(message_queue, mosquitto_client_instance, aws_client_instance)

try:
    mosquitto_client_instance.daemon = True
    aws_client_instance.daemon = True
    message_processor_instance.daemon = False
    mosquitto_client_instance.start()
    aws_client_instance.start()
    message_processor_instance.start()
except KeyboardInterrupt:
    print("Interrupted! Stopping threads...")
    mosquitto_client_instance.join()
    aws_client_instance.join()
    message_processor_instance.join()
