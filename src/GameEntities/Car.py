import random
from math import cos, sin, pi
import pygame
from pygame.math import Vector2


class Car:
    # original_image = pygame.transform.scale(original_image, (26, 41))
    SIZE = (26, 41)
    ORIGINAL_IMAGE_DIRS = [f"assets/images/car/car_{i}.png" for i in range(1, 5)]
    MAX_LINEAR_SPEED = 700  # maximum speed of the car
    RESISTENCE = MAX_LINEAR_SPEED * 0.25  # acceleration added to the car when no acceleration is added
    ACCELERATION = MAX_LINEAR_SPEED * 2 + RESISTENCE  # current car acceleration
    BRAKE_FORCE = ACCELERATION * 0.9  # acceleration added to the car when steering
    ANGULAR_SPEED: int = 6  # speed at which the car rotates expressed in degrees/second
    SHOCK_ABSORPTION_COEFFICIENT = 0.25  # percentage of remaining speed after hitting a wall
    
    def __init__(self, x, y, angle=pi):
        self.x = x
        self.y = y
        self.radius = 23
        self.angle = angle  # by default, the angle makes the car face upwards
        self.original_image = pygame.Surface((0, 0))  # the Surface given to the property will change after load_image()
        self.load_image()
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect()
        self.center = (self.x + self.SIZE[0], self.y + self.SIZE[1])
        self.hit_box = []

        self.linear_speed = 0  # a speed in pixels per second
        self.steering_direction: int = 0
        self.direction: int = 0  # 1: forward; -1: backwards; 0: no movement
        self.brake: int = 0  # if braking is activated it is set to 1 and makes the car brake (stop)

        self.keep_steering = False  # current steering state. Keeps steering in the steering direction if True
        self.keep_speeding = False  # keep speeding up status. Keeps speeding up in the current direction if True

    def load_image(self):
        self.original_image = pygame.image.load(random.choice(self.ORIGINAL_IMAGE_DIRS))
        if self.original_image.get_size() != self.SIZE:
            self.original_image = pygame.transform.scale(self.original_image, self.SIZE)
        self.original_image = self.original_image.convert_alpha()

    def steer(self, dt):  # clockwise: direction=1  | counterclockwise: dir = -1 | no change: dir = 0
        self.angle = (self.angle + self.steering_direction * self.ANGULAR_SPEED * dt)  # % 2*pi

    def update_speed(self, dt):
        a = self.direction * self.ACCELERATION  # acceleration
        movement_modulo = ((self.linear_speed > 0) - (self.linear_speed < 0))  # direction of the brakes (1 || -1)
        r = movement_modulo * (self.RESISTENCE + self.brake * self.BRAKE_FORCE)
        
        updated_speed = int(self.linear_speed + (a - r) * dt)  # V = V0 + (a - resistance)*t
        
        # guarantees that the speed is between the established limits
        self.linear_speed = min(self.MAX_LINEAR_SPEED, max(-self.MAX_LINEAR_SPEED, updated_speed))
        print(f"dir: {self.direction} | speed: {self.linear_speed} | accel: {a} | resist: {r} | mod: {movement_modulo}")

    def activate_speeding(self, direction, speeding_state=True):
        self.keep_speeding = speeding_state
        self.direction = direction

    def activate_steering(self, direction, steering_state=True):
        self.keep_steering = steering_state
        self.steering_direction = direction

    def activate_brakes(self, state=1):
        self.brake = state
    
    def activate_hitting_wall_effect(self):
        # the car is thrown in the opposite direction of the impact but with lower speed
        self.linear_speed *= -self.SHOCK_ABSORPTION_COEFFICIENT
        # make car immediately distance himself from wall
        self.x += self.linear_speed * sin(self.angle) * 0.05
        self.y += self.linear_speed * cos(self.angle) * 0.05
        
    def update_hit_box(self):
        rect = self.original_image.get_rect(center=self.center)
        pivot = pygame.math.Vector2(self.center)
        angle = -self.angle * 180 / pi
        self.hit_box = [(Vector2(rect.topleft) - pivot).rotate(angle) + pivot,
                        (Vector2(rect.topright) - pivot).rotate(angle) + pivot,
                        (Vector2(rect.bottomright) - pivot).rotate(angle) + pivot,
                        (Vector2(rect.bottomleft) - pivot).rotate(angle) + pivot]

    def update(self, dt):
        self.steer(dt)
        self.update_speed(dt)
        self.x += self.linear_speed * sin(self.angle) * dt
        self.y += self.linear_speed * cos(self.angle) * dt
        self.update_image()
        self.update_hit_box()

    def draw(self, screen):
        # drawing the car's hit-box
        pygame.draw.lines(screen, (255, 255, 0), True, self.hit_box, 1)  # hit-box of the car
        # drawing the car
        screen.blit(self.image, self.rect)

    def update_image(self):
        # offset from pivot to center
        image_rect = self.image.get_rect(topleft=(self.x - self.SIZE[0] / 2, self.y - self.SIZE[1] / 2))
        offset_center_to_pivot = pygame.math.Vector2((self.x, self.y)) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)

        # rotated image center
        self.center = (self.x - rotated_offset.x / 2, self.y - rotated_offset.y / 2)

        # get a rotated image
        self.image = pygame.transform.rotate(self.original_image, self.angle * 180 / pi)
        self.rect = self.image.get_rect(center=self.center)
