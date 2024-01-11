import pygame
from src.Utils.GAME_conf import SCREEN, BACKGROUND
from src.GameEntities import Car


class Game:
	cars = []
	
	def __init__(self):
		self.game_over_message = "The game reached an End"
		
		# Game Entities
		self.track_image = BACKGROUND
		self.car = Car(100, 350)
		self.cars.append(self.car)
		
		self.screen = SCREEN
		
		# game loop
		self.clock = pygame.time.Clock()
		self.dt = 0  # delta time: time between frames expressed in milliseconds
		self.is_running = True
	
	# ------------------------ Input Management --------------------------------
	def car_input_management(self, event):
		# managing when the player presses a button
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.car.activate_speeding(1)
			elif event.key == pygame.K_DOWN:
				self.car.activate_speeding(-1)
			elif event.key == pygame.K_SPACE:
				self.car.activate_brakes()
			elif event.key == pygame.K_RIGHT:
				self.car.activate_steering(-1, True)
			elif event.key == pygame.K_LEFT:
				self.car.activate_steering(1, True)
		
		# managing when the player releases a button
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				self.car.activate_speeding(0, False)
			elif event.key == pygame.K_SPACE:
				self.car.activate_brakes(0)
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				self.car.activate_steering(0, False)
	
	def mouse_input_management(self):
		# mouse_x, mouse_y = pygame.mouse.get_pos()
		
		# do what you want with mouse position here
		pass
	
	def manage_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False
			
			self.car_input_management(event)
		
		self.mouse_input_management()  # currently does nothing
	
	# ------------------------ Game Loop --------------------------------------
	def update(self):
		self.car.update(self.dt)
	
	def draw(self):
		self.screen.blit(self.track_image, (0, 0))
		self.car.draw(self.screen)
		pygame.display.update()
	
	def game_loop(self):
		while self.is_running:
			# Input management
			self.manage_input()
			
			# Game logic goes here
			
			self.update()
			self.draw()
			self.dt = self.clock.tick(60) / 1000  # updating delta time
		
		self.game_over()
	
	def game_over(self):
		pygame.quit()
		exit(self.game_over_message)


if __name__ == '__main__':
	game = Game()
	game.game_loop()
