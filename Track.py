import pygame
from util import load_image, scale_image, getPixelArray

class Track:
    
    def __init__(self):
        self.image = scale_image(load_image('track/track.png'),0.5)
        self.rect = self.image.get_rect()
        self.topleft = self.rect.topleft
        self.width, self.height = self.image.get_width(), self.image.get_height()
  
    
    def gettrack_dim(self):
        return self.width, self.height
    
    def get_image(self):
        return self.image

    def draw(self, surface):
        surface.blit(self.image, self.topleft)


    def get_Pixel_Array(self):
        return getPixelArray(self.image)
        
        

        