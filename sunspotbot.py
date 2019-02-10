import paho.mqtt.client as mqtt
import solace_client

import leapmotion_service


def onLeapmotion(self, message_content):
	client = mqtt.Client(transport="websockets")
	client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
	client.on_connect = solace_client.onConnect
	client.subscribe('leapmotion/')
	client.publish('leapmotion/', message_content)

	self.registrationMessage = self.service_registration_message(service_type)
	self.solace.sendMessage( + "/registration", self.registrationMessage)
	print("Connected!!")

def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onMessage(client, userdata, message):
	print('got message: ' + str(message.payload))

solace_client.init()
client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)


#if leapmotion
message_content = leapmotion.get_motion()
client.on_connect = onLeapmotion
client.on_disconnect = onDisconnect
client.on_message = onMessage


#if webapp


#if pi webcam



