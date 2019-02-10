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

        frame = controller.frame()

        THRESHOLD_X = 7.0
        THRESHOLD_Y = 7.0

        for current_hand in frame.hands:

            hand_speed = current_hand.palm_velocity
            hand_pos   = current_hand.stabilized_palm_position
            positions.append([hand_speed.x, hand_speed.z, hand_pos.x, hand_pos.z, hand_pos.y])

            break

        else:
            if len(positions) < 2:
                return

            # Send info to Arduino here

            def get_average(arr):
                return float(sum(arr)) / len(arr)

            def get_diff(arr, is_horizontal = False):

                # Given Bitonic Array Get Half

                direction = arr[1] >= arr[0]
                left = 1

                while left < len(arr) and (arr[left] >= arr[left - 1]) == direction:
                    left += 1

                return [arr[i] - arr[i - 1] for i in range(1, left)]

            def check_action(arr):
                # Compare Z positions

                BUFFER = len(arr) >> 1
                TOLERANCE = 50.0

                s = 0

                for i in arr[:BUFFER]:
                    for j in arr[-BUFFER:]:
                        if i - j > TOLERANCE:
                            s += 1
                        elif i - j < -TOLERANCE:
                            s -= 1

                if s > int(BUFFER**2 * 0.8):
                    return 1

                elif s < -int(BUFFER**2 * 0.8):
                    return -1

                return 0




            positions = list(zip(*positions))

            avg_vx = get_average(positions[0])
            avg_vy = get_average(positions[1])
            avg_x  = get_average(get_diff(positions[2]))
            action  = check_action(positions[3])
            positions = []

            direction = ""
            if avg_x > THRESHOLD_X:
                if action == 1:
                    # North East
                    direction = "NE"
                elif action == -1:
                    # South East
                    direction = "SE"
                else:
                    # East
                    direction = "E"
            elif avg_x < -THRESHOLD_X:
                if action == 1:
                    # North West
                    direction = "NW"
                elif action == -1:
                    # South West
                    direction = "SW"
                else:
                    # West
                    direction = "W"
            else:
                if action == 1:
                    # North
                    direction = "N"
                elif action == -1:
                    # South
                    direction = "S"

            self.send_data(direction, avg_vx, avg_vy)

    def send_data(self, direction, veloc_x, veloc_y):

        # Use this to send data
        print "sent"
        
        return

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
