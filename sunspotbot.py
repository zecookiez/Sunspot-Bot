import paho.mqtt.client as mqtt

from Leapmotion import leapmotion_service

def onConnect(client, userdata, flags, rc):
	print('subscribing')

def onLeapmotion(self, message_content):
	client.on_connect = onConnect
	client.subscribe('leapmotion/')
	client.publish('leapmotion/', message_content)

	self.registrationMessage = self.service_registration_message(service_type)
	self.solace.sendMessage( + "/registration", self.registrationMessage)
	print("Connected!!")

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


#if leapmotion
#recieve pub from leapmotion

message_content = leapmotion_service.get_motion()
client.on_connect = onLeapmotion
client.on_disconnect = onDisconnect
client.on_message = onMessage



#if webapp


#if pi webcam



