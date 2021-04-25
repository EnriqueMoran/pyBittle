"""An example of sending movements commands to Bittle through Bluetooth
connection.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..'))

from pyBittle import bittleManager  # noqa: E402


__author__ = "EnriqueMoran"


forward = bittleManager.Direction.FORWARD
forward_left = bittleManager.Direction.FORWARDLEFT
forward_right = bittleManager.Direction.FORWARDRIGHT

backward = bittleManager.Direction.BACKWARD
backward_left = bittleManager.Direction.BACKWARDLEFT
backward_right = bittleManager.Direction.BACKWARDRIGHT

walk = bittleManager.Gait.WALK
crawl = bittleManager.Gait.CRAWL
trot = bittleManager.Gait.TROT
run = bittleManager.Gait.RUN


def test_movement(bittle):
    """Send FORWARD, FORWARDLEFT and FORWARDRIGHT commands for every gait.
    """
    print(f"Sending command {forward}")
    bittle.send_movement_bluetooth(forward)
    time.sleep(3)

    print(f"Sending command {forward_left}")
    bittle.send_movement_bluetooth(forward_left)
    time.sleep(3)

    print(f"Sending command {forward_right}")
    bittle.send_movement_bluetooth(forward_right)
    time.sleep(3)


def test_backward(bittle):
    """Send BACKWARD, BACKWARDLEFT and BACKWARDRIGHT commands for the only
    avaliable backward gait, WALK.
    """
    print(f"Sending command {backward}")
    bittle.send_movement_bluetooth(backward)
    time.sleep(3)

    print(f"Sending command {backward_left}")
    bittle.send_movement_bluetooth(backward_left)
    time.sleep(3)

    print(f"Sending command {backward_right}")
    bittle.send_movement_bluetooth(backward_right)
    time.sleep(3)


if __name__ == '__main__':
    bittle = bittleManager.Bittle()
    print("Bittle instance created, connecting through Bluetooth...")
    isConnected = bittle.connect_bluetooth()

    if isConnected:
        print(f"Bittle connected: {bittle}")
        time.sleep(1)

        print("\nTest gait: WALK")
        print("----------------------")
        print(f"Setting gait {walk}")
        bittle.gait = walk
        time.sleep(1)
        test_movement(bittle)

        print("\nTest gait: CRAWL")
        print("----------------------")
        print(f"Setting gait {crawl}")
        bittle.gait = crawl
        time.sleep(1)
        test_movement(bittle)

        print("\nTest gait: TROT")
        print("----------------------")
        print(f"Setting gait {trot}")
        bittle.gait = trot
        time.sleep(1)
        test_movement(bittle)

        print("\nTest gait: RUN")
        print("----------------------")
        print(f"Setting gait {run}")
        bittle.gait = run
        time.sleep(1)
        test_movement(bittle)

        print("\nTest BACKWARD")
        print("----------------------")
        test_backward(bittle)

        print(f"Sending command {bittleManager.Command.BALANCE}")
        bittle.send_command_bluetooth(bittleManager.Command.BALANCE)
        time.sleep(2)

        print(f"Closing connection...")
        bittle.disconnect_bluetooth()
        print("Connection closed")
    else:
        print(f"Couldn't connect to Bittle")
