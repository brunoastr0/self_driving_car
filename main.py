import pygame
import sys
from Cars import Cars
from Colors import Colors
from Track import Track
from util import draw_track, getPixelArray

# Initialize Pygame


class Game:

    cars = []

    def __init__(self):

        pygame.init()
        self.track = Track()
        

        # Set up display
        WIDTH, HEIGHT = self.track.gettrack_dim()
       
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Base Project")
        self.screen_surf = pygame.display.get_surface()

        self.pixels = self.track.get_Pixel_Array()

        # print(self.color)
        # getPixelArray(self.track.get_image())

        draw_track(self.pixels,self.screen)

        # Main game loop
        self.clock = pygame.time.Clock()
        self.is_running = True


        

        self.car1 = Cars( 50,150, 4, self.pixels)
        self.cars.append(self.car1)

        

    

    def update(self,surface, players):
        for player in players:
            player.update(surface)
       


    def run(self):

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            # Game logic goes here
            # self.car1.collision(self.pixels)     

            
            
            
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
            
            

            # Drawing code
            
            
            # self.track.draw(self.screen)
            
            
            
            # Draw additional elements here
            
            self.update(self.screen, self.cars)
            
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

        # Quit Pygame and exit
        pygame.quit()
        sys.exit()


if __name__=='__main__':
    game = Game()
    game.run()