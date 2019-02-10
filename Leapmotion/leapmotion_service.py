import os, sys, inspect, thread, time

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
        :return [veloc_x, veloc_y]:
        """

        frame = controller.frame()

        THRESHOLD_X  = 450.0
        NORTH_THRESH = -500.0
        SOUTH_THRESH = 800.0

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
            avg_vy = get_average(positions[1])
            avg_vz = get_average(positions[2])
            

            positions = []

            direction = ""
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
            else:
                if avg_vz < NORTH_THRESH:
                    # North
                    direction = "N"
                elif avg_vz > SOUTH_THRESH:
                    # South
                    direction = "S"

            self.send_data(direction, avg_vx, avg_vy)

    def send_data(self, direction, veloc_x, veloc_y):

        # Use this to send data
        print direction

        return

def main():

    # START



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
