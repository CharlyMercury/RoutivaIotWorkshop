from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import threading
import json
import sys


class AwsMqttClient(threading.Thread):

    def __init__(self, endpoint_, port_, cert_, key_, ca_, client_id_,
                 topics_, parameters_, message_queue, proxy_host=None, proxy_port=None):
        threading.Thread.__init__(self)
        self.message_queue = message_queue
        self.topics = topics_
        self.count = 0
        self.plantel = parameters_["client"]
        proxy_options = None
        if proxy_host is not None and proxy_port != 0:
            proxy_options = http.HttpProxyOptions(
                host_name=proxy_host,
                port=proxy_port)

        # Create a MQTT connection from the command line data
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=endpoint_,
            port=port_,
            cert_filepath=cert_,
            pri_key_filepath=key_,
            ca_filepath=ca_,
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
            client_id=client_id_,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=proxy_options,
            on_connection_success=self.on_connection_success,
            on_connection_failure=self.on_connection_failure,
            on_connection_closed=self.on_connection_closed)

        # print(f"Connecting to {endpoint_} with client ID '{client_id_}'...")
        connect_future = self.mqtt_connection.connect()
        # Future.result() waits until a result is available
        connect_future.result()
        # print("Connected!")

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(self, connection, error, **kwargs):
        self.count = 0
        print("Connection interrupted. error: {}".format(error))

    # Callback when the subscribed topic receives a message
    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs):
        self.count = 0
        # print("Received message from AWS topic '{}': {}".format(topic, payload))
        # Put the message in the queue
        self.message_queue.put(("aws", topic, payload))

    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        # print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self.on_resubscribe_complete)

    def on_resubscribe_complete(self, resubscribe_future):
        self.count = 0
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic_, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic_))

    # Callback when the connection successfully connects
    def on_connection_success(self, connection, callback_data):
        self.count = 0
        assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
        print("Connection Successful with return code: {} session "
              "present: {}".format(callback_data.return_code, callback_data.session_present))

    # Callback when a connection attempt fails
    def on_connection_failure(self, connection, callback_data):
        self.count = 0
        assert isinstance(callback_data, mqtt.OnConnectionFailureData)
        print("Connection failed with error code: {}".format(callback_data.error))

    # Callback when a connection has been disconnected or shutdown successfully
    def on_connection_closed(self, connection, callback_data):
        self.count = 0
        print("Connection closed")

    def subscribe_to_topics(self):
        # Subscribe for a list of topics
        print(f"Aws Client Subscribed to topics: {self.topics}")
        for topic_sub in self.topics:
            subscribe_future, packet_id = self.mqtt_connection.subscribe(
                topic=topic_sub,
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_message_received)
            subscribe_result = subscribe_future.result()
            # print("Subscribed with {}".format(str(subscribe_result['qos'])))

    def publish_to_topics(self, topic_pub_, input_message: dict):
        # Publish message to broker server.
        if input_message:
            # print("Publishing message to topic '{}': {}".format(topic_pub_, input_message))
            message_json = json.dumps(input_message)
            self.mqtt_connection.publish(
                topic=topic_pub_,
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE)

    def run(self):
        self.subscribe_to_topics()
        while True:
            pass
