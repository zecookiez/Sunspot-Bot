import os, sys, inspect, thread, time
import paho.mqtt.client as mqtt
import ssl

PATH = os.path.dirname(os.path.realpath(__file__)) + "/LeapSDK/lib"
sys.path.insert(0, PATH)
arch_dir = '/x64' if sys.maxsize > 2**32 else '/x86'
sys.path.insert(0, PATH + arch_dir)

import Leap

class EventListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"
        return None


    global positions

    positions = []

    def on_frame(self, controller):

        global positions

        """
        :param controller:
        :return [direction, veloc_x, veloc_y]:
        """

        frame = controller.frame()
        
        """For Sitting Down Purposes Use:
        THRESHOLD_X = 200
        NORTH_THRESH = -200
        SOUTH_THRESH = 200"""

        THRESHOLD_X  = 300.0
        NORTH_THRESH = -200.0
        SOUTH_THRESH = 500.0

        for current_hand in frame.hands:

            hand_speed = current_hand.palm_velocity
            hand_pos   = current_hand.stabilized_palm_position
            positions.append([hand_speed.x, hand_speed.z, hand_speed.y])

            break

        else:

            if len(positions) < 2:
                return

            def get_average(arr):
                middle = len(arr) >> 1
                return float(sum(arr[:middle])) / len(arr[:middle])

            positions = list(zip(*positions))

            avg_vx = get_average(positions[0])
            avg_vz = get_average(positions[2])

            print avg_vx, avg_vz

            positions = []

            direction = "STOP"
            if avg_vx > THRESHOLD_X:
                if avg_vz < NORTH_THRESH - 100.0:
                    # North East
                    direction = "NE"
                elif avg_vz > SOUTH_THRESH - 100.0:
                    # South East
                    direction = "SE"
                else:
                    # East
                    direction = "E"
                    avg_vz = 0

            elif avg_vx < -THRESHOLD_X:
                if avg_vz < NORTH_THRESH - 100.0:
                    # North West
                    direction = "NW"
                elif avg_vz > SOUTH_THRESH - 100.0:
                    # South West
                    direction = "SW"
                else:
                    # West
                    direction = "W"
                    avg_vz = 0
            else:
                if avg_vz < NORTH_THRESH:
                    # North
                    direction = "N"
                    avg_vx = 0

                elif avg_vz > SOUTH_THRESH:
                    # South
                    direction = "S"
                    avg_vx = 0

            avg_vx = min(255, int(abs(avg_vx) * 255 / 1800))
            avg_vz = min(255, int(abs(avg_vz) * 255 / 1000))

            self.send_data(direction, avg_vx, avg_vz)

    def onConnect(client, userdata, flags, rc):
        print ("connected.")


    def onDisconnect(client, userdata, rc):
        print('disconnected!')

    def onMessage(client, userdata, message):
        print('got message: ' + str(message.payload))

    def send_data(self, direction, veloc_x, veloc_y):

        # send pub to sunspotbot
        client = mqtt.Client(transport="websockets")
        client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
        client.on_connect = self.onConnect
        client.on_disconnect = self.onDisconnect

        cwd = os.getcwd()
        connections='C:/Users/Zeyu/Desktop/Sunspot-Bot/solace.cloud'
        connection_args = {}
        with open(connections, "r") as f:
            for line in f:
                (key, val) = line.strip().split('=')
                connection_args[key] = val

        client.username_pw_set(connection_args['username'], password=connection_args['password'])
        client.connect(connection_args['url'], int(connection_args['port']), 20)
        
        if direction: 
            message = direction + " " + str(min(max(veloc_x, 90), 255)) + " " + str(min(max(veloc_y, 90), 255))
            client.publish("leapmotion/motion", message)

def main():
    
    # Create a sample listener and controller
    listener = EventListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

main()
