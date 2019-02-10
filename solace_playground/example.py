import paho.mqtt.client as mqtt
import ssl

def onConnect(client, userdata, flags, rc):
	print('connected!')
	print('subscribing to topic')
	client.subscribe('test')
	print('publishing to topic')
	client.publish('test', 'hello world!')

def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onMessage(client, userdata, message):
	print('got message: ' + str(message.payload))

client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.username_pw_set('solace-cloud-client', password='randompassword')
client.connect('mr4b11zra4x.messaging.mymaas.net', 8443, 20)
client.loop_forever()