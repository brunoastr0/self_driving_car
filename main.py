import pygame
import sys
from Cars import Cars
from Colors import Colors
from Track import Track
from util import draw_track, getPixelArray
from qlearning import QLearning
import math

# Initialize Pygame


class Game:

    cars = []
    NUM_ACTIONS = 5
    ACTIONS = {0:"UP",1:'DOWN',2:'RIGHT',3:'LEFT',4:'DEACC'}
    CAR_BRAIN_QTD_INPUT = 10  # Replace with your actual value
    DEGTORAD = math.pi / 180.0  # Conversion factor from degrees to radians

    def __init__(self):

        pygame.init()
        self.track = Track()
        

        # Set up display
        self.WIDTH, self.HEIGHT = self.track.gettrack_dim()
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Base Project")
        # self.screen_surf = pygame.display.get_surface()

        self.pixels = self.track.get_Pixel_Array()
        # self.agent = QLearning()
        # print(self.color)
        # getPixelArray(self.track.get_image())


        # Main game loop
        self.clock = pygame.time.Clock()
        self.is_running = True


        

        self.car1 = Cars( 100,150, 4, self.pixels)
        self.cars.append(self.car1)

        

    

    def update(self,surface, players):
        for player in players:
            player.update(surface)
       
    def aplicarSensores(self,car, pixels):
        for i in range(18):
            X1, Y1 = car.middle
            self.angle = abs(car.angle) - 90.0 + (i * 180.0 / (18-2))    

            Adjacente = math.cos(math.radians(self.angle))
            Oposto = math.sin(math.radians(self.angle))
            

            while True:
                X1 = X1 + Oposto
                Y1 = Y1 + Adjacente
                
                if pixels[int(X1)][int(Y1)] == 0:
                    
                    X1 = X1 - Adjacente
                    Y1 = Y1 - Oposto
                    dist = self.DistanciaEntrePontos(car.middle[0], car.middle[1], X1, Y1)
                    car.sensors[i] = (dist)          
                    break
            #     # print(car.sensors)
            print(f"Sensor {i}: {car.sensors[i]}, X1: {X1}, Y1: {Y1}, angle: {self.angle}")

    # Assuming you have a DistanciaEntrePontos function implemented elsewhere
    def DistanciaEntrePontos(self,x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
   



    def draw_lines_and_sprites(self,car):
        self.aplicarSensores(self.car1, self.pixels)
        x,y = car.middle
        for i in range(18 - 1):
            sensor_angle = car.angle - 90 + i * 180 / (18 - 1) 
            X = car.middle[0] + car.sensors[i] * math.cos(math.radians(sensor_angle - 90.0 + ((180.0 / (18 - 2)) * i)))
            Y = car.middle[1] + car.sensors[i] * math.sin(math.radians (sensor_angle - 90.0 + ((180.0 / (18 - 2)) * i)))
           
            pygame.draw.line(self.screen,Colors.YELLOW.value, (x,y), (X, Y))

            # if i < self.CAR_BRAIN_QTD_INPUT / 4 or i > 3 * self.CAR_BRAIN_QTD_INPUT / 4:
            #     # Assuming DesenharLinhaSimples and DesenharSprite functions are defined elsewhere
            
            # else:
            #     pygame.draw.line(self.screen,Colors.RED.value, (car.middle), (X, Y))


    def run(self):

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            # Game logic goes here
            # self.car1.collision(self.pixels)     

            
            # self.aplicarSensores(self.car1, self.pixels)

            moved = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                moved = True
                self.car1.drive('UP')
            
            if keys[pygame.K_LEFT]:
                self.car1.drive('LEFT')

            if keys[pygame.K_RIGHT]:
             
                self.car1.drive('RIGHT')
            
            if keys[pygame.K_DOWN]:
                self.car1.drive('DOWN')

            if not moved:
                self.car1.drive('DEACC')
            
            
            mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get the color at the mouse position on the screen
            color_at_mouse = self.screen.get_at((mouse_x, mouse_y))
            # Drawing code
            # print(color_at_mouse)
            self.screen.fill(Colors.BLACK.value)
            self.track.draw(self.screen)
            
            self.draw_lines_and_sprites(self.car1)

            
            # Draw additional elements here
            
            self.update(self.screen, self.cars)
            
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)
            # p.display.flip()
        # Quit Pygame and exit
        pygame.quit()
        sys.exit()


if __name__=='__main__':
    game = Game()
    game.run()