import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
# rc is return code
class SolaceClient:

    def __init__(self,connection_properties='./solace.cloud'):
        self.isConnected = 0

    def on_connect_callback(client, userdata, rc):
        print("Connected, subscribing...")
        print("rc: " + str(rc))
        self.isConnected = 1;

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    def on_disconnect_callback(client, userdata, rc):
        print('Disconnected')
        print("rc: " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message_callback(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def on_publish_callback(mqttc, obj, mid):
        print(str(mid))

    def on_subscribe_callback(mqttc, obj, mid, granted_qos):
        print("Subscribed to: " + str(mid) + " " + str(granted_qos))

    def on_log_callback(mqttc, obj, level, string):
        print(string)

    def send_message(topic, message):
        client.publish(topic, message)

    print ("cries in chinese")

    self.client = mqtt.Client(transport="websockets")
    self.client.username_pw_set(props['solace-cloud-client'], password=props['a3180gpmn9jklddoq3kbrbsg4'])
    self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)

    self.client.subscribe("leapmotion/#") = on_subscribe_callback
    self.client.on_message = on_message_callback
    self.client.on_connect = on_connect_callback
    self.clent.on_publish = on_publish_callback
    self.clent.on_subscribe = on_subscribe_callback

    self.client.on_log = on_log_callback
    self.client.connect("leapmotion-service.messaging.mymaas.net", 8443, 20)


    # client.on_disconnect = on_disconnect_callback
    # client.on_message = on_message_callback
    # message = new MqttMessage("Hello world from MQTT!".getBytes());


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()



