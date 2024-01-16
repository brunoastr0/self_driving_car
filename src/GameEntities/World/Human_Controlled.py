import pygame
from src.GameEntities.World.Base import World_Base
from src.GameEntities import Car


class World_Human_Controlled(World_Base):
	def __init__(self):
		super().__init__()
		self.car = Car(100, 350)
		print("Human Controlled World Has Been Created")
	
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
			elif event.key == pygame.K_LEFT:
				self.car.activate_steering(1)
			elif event.key == pygame.K_RIGHT:
				self.car.activate_steering(-1)
		
		# managing when the player releases a button
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				self.car.activate_speeding(0)
			elif event.key == pygame.K_SPACE:
				self.car.activate_brakes(0)
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				self.car.activate_steering(0)
	
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
	