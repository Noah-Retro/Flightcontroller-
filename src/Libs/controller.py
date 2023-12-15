import os
import pprint
import pygame
from queue import Queue

"""
0:"X"
1:"O"
2:Dreieck
3:Quadrat
4:L1
5:R1
6:L2
7:R2
8:share
9:option
10:PS button
11:L3
12:R3
Axisdata:Axis on L and R Down {0,1} UP {0,-1} right {1,0} left {-1,0} data {{x,y},{x,y}} {L,R}
hat_data:Dpad axis Up {0,1} Down {0,-1} right {1,0} left {-1,0}
"""

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    
    def __init__(self,q:Queue):
        self.queue = q
        self.controller = None
        self.axis_data = None
        self.button_data = None
        self.hat_data = None

    def init(self):
        """Initialize the joystick components"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                print("gets data in controller")
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                self.queue.put({**self.button_data,**self.axis_data,**self.hat_data})
                return 
                os.system('clear')
                pprint.pprint(self.button_data)
                pprint.pprint(self.axis_data.keys())
                pprint.pprint(self.hat_data.keys())


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()