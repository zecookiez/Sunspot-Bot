import paho.mqtt.client as mqtt

from Leapmotion import leapmotion_service

def onConnect(client, userdata, flags, rc):
	print('subscribing')

def onDisconnect(client, userdata, rc):
	print('disconnected!')

def onLeapmotion(topic_name, message_content):
	client.on_connect = onConnect
	client.subscribe(topic_name)
	client.publish(topic_name, message_content)

	self.registrationMessage = self.service_registration_message(service_type)
	self.solace.sendMessage( + "/registration", self.registrationMessage)
	print("sent!!")

def onMessage(client, userdata, message):
	print('got message: ' + str(message.payload))

	if (str(message.topicName) == 'webcam/'):

	if (str(message.topicName) == 'leapmotion/motion'):
		client.on_connect = onLeapmotion('leapmotion/motion_raw', str(message.payload))
		client.on_disconnect = onDisconnect
	elif (str(message.topicName) == 'leapmotion/stop'): #from leap, TODO
		client.on_connect = onLeapmotion('leapmotion/stop_raw', "STOP ")
	elif (str(message.topicName) == 'leapmotion/interrupt_clear'): #from webapp, TODO
		client.on_connect = onLeapmotion('leapmotion/interrupt_clear_raw', "OVERRIDE ")


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


#if webapp

#if pi webcam



