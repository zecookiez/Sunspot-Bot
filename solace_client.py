import paho.mqtt.client as mqtt
import ssl


def onConnect(client, userdata, flags, rc):
	print('subscribing to topic: ' + subscribe_topic)
	client.subscribe(subscribe_topic)
	print('publishing' + msg)
	client.publish(subscribe_topic, msg)

def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onMessage(client, userdata, message):
	print('got message: ' + str(message.payload))


connections='./solace.cloud'
connection_args = {}
with open(connections, "r") as f:
    for line in f:
        (key, val) = line.strip().split('=')
        connection_args[key] = val


client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.username_pw_set(connection_args['username'], password=connection_args['password'])
client.connect(connection_args['url'], int(connection_args['port']), 20)

client.loop_forever()

