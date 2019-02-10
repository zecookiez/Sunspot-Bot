import numpy as np
import cv2
import paho.mqtt.client as mqtt
import ssl


def onConnect(client, userdata, flags, rc):
	print ("connected.")

def onPublish(message):
	print('publishing...')
	client.publish("webcam", message)

def onDisconnect(client, userdata, rc):
	print('disconnected!')

client = mqtt.Client(transport="websockets")
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)

connections='./solace.cloud'
connection_args = {}
with open(connections, "r") as f:
	for line in f:
		(key, val) = line.strip().split('=')
		connection_args[key] = val

client.username_pw_set(connection_args['username'], password=connection_args['password'])
client.connect(connection_args['url'], int(connection_args['port']), 20)
client.on_connect = onConnect
client.on_disconnect = onDisconnect

cap = cv2.VideoCapture(0)
array = []
delay = 0

while(True):
	trash, frame = cap.read()

	client.on_publish = onPublish(str(frame))
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()