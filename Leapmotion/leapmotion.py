import os, sys, inspect, thread, time

PATH = os.path.dirname(os.path.realpath(__file__)) + "/LeapSDK/lib"
sys.path.insert(0, PATH)
arch_dir = '/x64' if sys.maxsize > 2**32 else '/x86'
sys.path.insert(0, PATH + arch_dir)

import Leap

class EventListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"

    global DELAY

    DELAY = 0
    def on_frame(self, controller):

        """
        :param controller:
        :return [veloc_x, veloc_y]:
        """

        global DELAY
        DELAY -= 1

        frame = controller.frame()

        if DELAY > 0:
            return

        THRESHHOLD = 300.0

        for current_hand in frame.hands:

            hand_speed = current_hand.palm_velocity

            if abs(hand_speed.x) < THRESHHOLD > abs(hand_speed.y):
                return 0, 0

            # Send info to Arduino here
            DELAY = 60
            
            return hand_speed.x, hand_speed.y


def main():
    # Create a sample listener and controller
    listener = EventListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

main()
