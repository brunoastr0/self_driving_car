import pygame

pygame.display.set_caption("Pygame Base Project")
TRACK_IMAGE_DIR = "assets/images/track/track.png"
TRACK_IMAGE = pygame.image.load(TRACK_IMAGE_DIR)
WIDTH, HEIGHT = 800, 800
BACKGROUND = pygame.transform.scale(TRACK_IMAGE, (WIDTH, HEIGHT))
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
