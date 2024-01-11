import pygame
from pygame import Vector2
from Colors import Colors
from util import scale_image, blit_rotate_center, load_image
import math


class Cars:
    MAX_VEL = 5
    MOVED = False
    NUM_VISION = 18

    def __init__(self, x, y, rotation_vel, pixels):

        self.velocity = 0
        self.color = Colors.YELLOW.value
        self.image = scale_image(self.car_image(),0.05)
        self.rect = self.image.get_rect(center=(x,y))
        self.position = Vector2(x,y)
        self.middle = self.rect.center
        self.angle = 0
        self.rotation_vel = rotation_vel
        self.aceleration = 0.1
        self.deaceleration = 0.05
        self.direction = "STOP"
        self.pixels = pixels
        self.vision = self.NUM_VISION
        self.sensors = [0]*self.NUM_VISION

        
         


    def car_image(self):
        return load_image("car/car1.png")
    
    def draw(self, surface):
        # pygame.draw.rect(surface,Colors.BLUE.value ,self.rect)
        blit_rotate_center(surface, self.image, self.angle, self.position)

    
    def rotate(self, LEFT=False, RIGHT=False):
        if LEFT:
            self.angle += self.rotation_vel
        elif RIGHT:
            self.angle -= self.rotation_vel

    def drive(self, event):
        
        directions = {None: self.direction,"UP":"UP", "DOWN":"DOWN", "LEFT":"LEFT", "RIGHT":"RIGHT", "DEACC":"DEACC"}
        self.direction = directions[event]
        if self.direction == "UP":
            self.MOVED = True
            self.move_forward()
        elif self.direction == "DOWN":
            self.car_brake()
        if self.direction == "LEFT":
            self.rotate(LEFT=True)
        elif self.direction == "RIGHT":
            self.rotate(RIGHT=True)
        if self.direction == "DEACC":
            self.deacelerate()
        

    def move_forward(self):
        self.velocity = min(self.velocity+self.aceleration, self.MAX_VEL)
        self.move()

    


    def move(self):

        if self.collide(self.pixels):
                self.bounce()

        radians = math.radians(self.angle)
        vertical  = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        self.position.x -= horizontal
        self.position.y -= vertical
        
        # Update the rect based on the new position
        self.rect.center = (int(self.position.x + self.image.get_width() / 2), int(self.position.y + self.image.get_height() / 2))
        self.middle = self.rect.center

        

    def deacelerate(self):

        self.velocity = max(self.velocity - self.deaceleration, 0)
        self.move()

    def car_brake(self):
        self.velocity = max((self.velocity - self.deaceleration)/2, 0)
        self.move()

    def bounce(self):
        self.velocity = - self.velocity
        # self.move()


    def update(self, surface):
        # Update logic goes here
        #self.rotate()
        self.draw(surface)

    
    def collide(self, pixels):
        self.x, self.y = self.position
        
        if pixels[(round(self.y))][(round(self.x))] == 1:
            # self.move(collision=True)
            # print(self.x, self.y)
            return False
        return True
     
            
   

  

    # Assuming CAR_BRAIN_QTD_INPUT and cenario are defined somewhere
    # and you have a Carro class with attributes X, Y, Angulo, and DistanciaSensores

                    
                



        


    
    
