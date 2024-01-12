import pygame
from src.GameEntities.World.Base import World_Base


class World_AI_Testing(World_Base):
	def __init__(self):
		super().__init__()
		print("AI Testing World Has Been Created")
