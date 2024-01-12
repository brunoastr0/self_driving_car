import pygame
from src.Utils.GAME_conf import SCREEN, BACKGROUND


class World_Base:
	def __init__(self):
		self.game_over_message = "The game reached an End"
		
		# Game Entities
		self.track_image = BACKGROUND
		
		self.screen = SCREEN
		
		# game loop
		self.clock = pygame.time.Clock()
		self.dt = 0  # delta time: time between frames expressed in milliseconds
		self.is_running = True
	
	# ------------------------ Input Management --------------------------------
	def manage_input(self):
		pass
	
	# ------------------------ Game Loop --------------------------------------
	def update(self):
		pass
	
	def draw(self):
		pass
	
	def game_loop(self):
		while self.is_running:
			
			# Input management
			self.manage_input()
			
			self.update()
			self.draw()
			self.dt = self.clock.tick(60) / 1000  # updating delta time
		
		self.game_over()
	
	def game_over(self):
		pygame.quit()
		exit(self.game_over_message)
