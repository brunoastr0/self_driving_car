import pygame
from src.GameEntities.World.Base import World_Base


class World_AI_Training(World_Base):
	def __init__(self):
		super().__init__()
		print("AI Training World Has Been Created")
