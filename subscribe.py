import paho.mqtt.client as mqtt
import ssl
#import serial, time
#arduino = serial.Serial('/dev/ttyUSB0',9600,timeout=0.1)
 
 
def onSubscribe(topic_name):
    print("subscribed!")
   
def onConnect(client, userdata, flags, rc):
    print('connected, subscribing...')
    client.subscribe('leapmotion/motion')
    client.subscribe('leapmotion/stop_raw')
    client.subscribe('leapmotion/interrupt_clear_raw')
    print("subscribedc")
 
 
def onDisconnect(client, userdata, rc):
    print('disconnected!')
 
def onMessage(client, userdata, message):
    print('got message: ' + str(message.payload))
 
    if (str(message.topicName) == 'leapmotion/motion'):
    #   print('got message: ' + str(message.payload))
        arduino.write(message.payload)
    elif (str(message.topicName) == 'leapmotion/stop_raw'):
    #   print('got message: ' + str(message.payload))
        arduino.write("STOP ")
    elif (str(message.topicName) == 'leapmotion/interrupt_clear_raw'):
    #   print('got message: ' + str(message.payload))
        arduino.write("TAKEOVER ")
 
 
connections='/home/pi/Sunspot-Bot/solace.cloud'
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