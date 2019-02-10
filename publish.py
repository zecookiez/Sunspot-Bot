import paho.mqtt.client as mqtt
import ssl


def onConnect(client, userdata, flags, rc):
	print ("connected.")

def onPublish(body):
	print('publishing...')
	client.publish("testing/client", body)

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
client.on_connect = print("connected.")
client.on_disconnect = print('disconnected!')
client.on_message = print('got message: ' + str(message.payload))

client.username_pw_set(connection_args['username'], password=connection_args['password'])
client.connect(connection_args['url'], int(connection_args['port']), 20)


# for i in range(0,10):
client.on_publish = onPublish("test")
client.on_publish = onPublish("test1")
client.on_publish = onPublish("test2")
client.on_publish = onPublish("test3")
# 	client.on_message = onMessage


client.loop_forever()

