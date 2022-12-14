from GraphController import GraphController
from pygame.locals import *
from datetime import datetime
import pygame
class pygameController:
    def __init__(self):
        self.currentInput = ""
        self.capturingInput = False

    def toggleInput(self):
        self.capturingInput = not self.capturingInput
        self.currentInput = ""

    def run_game(self):
        self.G = GraphController()
        start = datetime.now()
        self.G.refresh()
        end = datetime.now()
        print('Time to draw stars: ', end - start)
        while True:
            pygame.display.update()
            self.G.updateInfoText()
            events = pygame.event.get()
            if self.capturingInput:
                for event in events:
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            #return
                            print(self.currentInput)
                            self.toggleInput()
                        elif event.key == K_BACKSPACE:
                            self.currentInput = self.currentInput[:-1]
                        else:
                            self.currentInput += event.unicode
            else:
                self.G.handleKeys(events)

P = pygameController()
P.run_game()