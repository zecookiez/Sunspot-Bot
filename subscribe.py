import paho.mqtt.client as mqtt
import ssl


def onConnect(client, userdata, flags, rc):
	print('connected, subscribing...')
	client.on_subscribe('leapmotion/motion_raw')
	client.on_subscribe('leapmotion/stop_raw')
	client.on_subscribe('leapmotion/interrupt_clear_raw')


def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onMessage(client, userdata, message):
	print('got message: ' + str(message.payload))

	if (str(message.topicName) == 'leapmotion/motion_raw'):

	elif str(message.topicName) == 'leapmotion/stop_raw'):
	
	elif str(message.topicName) == 'leapmotion/interrupt_clear_raw'):


def onSubscribe(topic_name)

connections='./solace.cloud'
connection_args = {}
with open(connections, "r") as f:
    for line in f:
        (key, val) = line.strip().split('=')
        connection_args[key] = val

client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.on_connect = onConnect

client.username_pw_set(connection_args['username'], password=connection_args['password'])
client.connect(connection_args['url'], int(connection_args['port']), 20)

client.loop_forever()

