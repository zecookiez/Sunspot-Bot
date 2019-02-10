import paho.mqtt.client as mqtt

class SolaceMQTTClient:
    
    def __init__(self, connections='./solace.cloud'):
        connection_args = {}
        with open(connections, "r") as f:
            for line in f:
                (key, val) = line.strip().split('=')
                connection_args[key] = val

        self.client = mqtt.Client()

        def onConnect(client, userdata, flags, rc):
            self.onConnect(client, userdata, flags, rc)
        
        def onDisconnect(client, userdata, rc):
            print('Disconnected')
            print("rc: " + str(rc))
        
        def onMessage(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))
            self.processRxMessage(client, userdata, msg)

        def onLog(client, userdata, level, buf):
            print(buf)

        self.client.on_connect = onConnect
        self.client.on_disconnect = onDisconnect
        self.client.on_message = onMessage
        self.client.on_log = onLog
        self.client.username_pw_set(connection_args['username'], password=connection_args['password'])
        self.client.connect(connection_args['url'], int(connection_args['port']), 20)
        self.client.loop_start()
        
    def publish(self, topic, body):
        self.client.publish(topic, body)

    def subscribe(self, topic): #topic must be string
        print("Subscribing to: " + topic)
        self.client.subscribe(topic)
            
    def sendResponse(self, rxMessage, txMessage):
        topic                 = self.makeReplyTopic(rxMessage['client_id'])
        txMessage['msg_type'] = rxMessage['msg_type'] + "_response"
        # txMessage['msg_id']   = rxMessage['msg_id']
        self.sendMessage(topic, txMessage)

    def sendMessage(self, topic, message, callback=None, timeout=0, retries=0):
        txMessage                 = copy.deepcopy(message)
        self.client.publish(topic, payload=json.dumps(txMessage))

        
    def onConnect(self, client, userdata, flags, rc):
        if rc != 0:
            raise NameError("Failed to connect: " + str(rc))

        self.subscribe('leapmotion/p2p/')
        print("Connected, subscribed, publishing...")
        self.publish('leapmotion/p2p/', 'hello world!')
        print("return code: " + str(rc))

    def processRxMessage(self, client, userdata, msg):
        payload = msg.payload.decode()
        # pprint.pprint(payload)
        # try:
        #     rxMessage = json.loads(payload)
        # except ValueError:
        #     print("Failed to parse message: ")
        #     print(payload)
        #     return
        
        # if 'msg_type' not in rxMessage:
        #     print('Received message with no msg_type')
        #     return

        # if 'client_id' not in rxMessage:
        #     print('Received message with no client_id')
        #     return
        
        # if 'current_time' not in rxMessage:
        #     print('Received message with no current_time')
        #     return
        
        # if 'msg_id' not in rxMessage:
        #     print('Received message with no msg_id')
        #     return

        msgType = rxMessage['msg_type']
        # msgId   = rxMessage['msg_id']

        if msgType == "ping":
            self.sendResponse(rxMessage, {})
        elif re.search('_response', msgType) and msgId in self.pendingReplies:
            info = self.pendingReplies[msgId]
            info.timer.cancel()
            info.callback(info.txMessage, rxMessage)
        else:
            if msgType in self.callbacks:
                self.callbacks[msgType](msg.topic, rxMessage)
            else:
                print("Unhandled message type:" + msgType)

    def makeReplyTopic(self, clientId):
        return "leapmotion/p2p/" + str(clientId)
