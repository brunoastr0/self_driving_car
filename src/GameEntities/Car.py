import random
from math import cos, sin, pi, hypot
import pygame
from pygame.math import Vector2
from src.Utils.COLORS import OBSTACLE_COLORS


class Car:
    # original_image = pygame.transform.scale(original_image, (26, 41))
    SIZE = (26, 41)  # size of the car (width, length)
    ORIGINAL_IMAGE_DIRS = [f"assets/images/car/car_{i}.png" for i in range(1, 5)]  # directories of akk the car's images
    MAX_LINEAR_SPEED = 700  # maximum speed of the car: pixel/second
    RESISTENCE = MAX_LINEAR_SPEED * 0.35  # deceleration (makes car slowly stop when not accelerating): pixel/(second^2)
    ACCELERATION = MAX_LINEAR_SPEED * 2   # acceleration: pixel/(second^2)
    BRAKE_FORCE = ACCELERATION * 0.9  # deceleration added to the car when brakes are used: pixel/(second^2)
    ANGULAR_SPEED: int = 6  # speed at which the car rotates: degrees/second
    SHOCK_ABSORPTION_COEFFICIENT = 0.25  # percentage of remaining speed after hitting a wall

    VISION_ANGLES = {"front": 90, "left": 0, "right": 180, "front-left": 45, "front-right": 135}  # degrees
    DEATH_DISTANCE = {"front": 20, "left": 7, "right": 7, "front-left": 29, "front-right": 29}    # units
    VISION_STEP = 1  # unitary distance between each vision step. A lower value means more precise vision at higher cost
    VISION_RANGE = 1000
    
    def __init__(self, x, y, angle=pi):
        self.x = x
        self.y = y
        self.radius = 23
        self.angle = angle  # by default, the angle makes the car face upwards
        
        self.original_image = pygame.Surface((0, 0))  # the Surface given to the property will change after load_image()
        self._load_image()
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect()
        self.center = (self.x + self.SIZE[0], self.y + self.SIZE[1])
        self.hit_box = []

        self.linear_speed = 0  # a speed in pixels per second
        self.steering_direction: int = 0
        self.engine_force_direction: int = 0  # engine's force direction: 1-> forward; -1-> backwards; 0-> no movement
        self.brake: int = 0  # if braking is activated it is set to 1 and makes the car brake (stop)

        self.keep_steering = False  # current steering state. Keeps steering in the steering direction if True
        self.keep_speeding = False  # keep speeding up status. Keeps speeding up in the current direction if True
        
        self.alive = True

    def _load_image(self):
        self.original_image = pygame.image.load(random.choice(self.ORIGINAL_IMAGE_DIRS))
        if self.original_image.get_size() != self.SIZE:
            self.original_image = pygame.transform.scale(self.original_image, self.SIZE)
        self.original_image = self.original_image.convert_alpha()
    
    # ----------------------- Movement Control Methods --------------------------
    # These methods act as a kind of API for controlling the car.
    # (external) Events affecting the car's movement should trigger the use of one of the methods of this section
    
    def activate_speeding(self, direction):
        self.keep_speeding = direction != 0
        self.engine_force_direction = direction

    def activate_steering(self, direction):
        self.keep_steering = direction != 0
        self.steering_direction = direction

    def activate_brakes(self, state=1):
        self.brake = state
    
    def activate_hitting_wall_effect(self):
        # the car is thrown in the opposite direction of the impact but with lower speed
        self.linear_speed *= -self.SHOCK_ABSORPTION_COEFFICIENT
        # make car immediately distance himself from wall
        self.x += self.linear_speed * sin(self.angle) * 0.05
        self.y += self.linear_speed * cos(self.angle) * 0.05
    
    # --------------------------- Collision and Vision -------------------------
  
    def get_distance(self, screen: pygame.Surface, vision_type: str):
        additional_angle = self.VISION_ANGLES[vision_type]
        vision_ray_end_x, vision_ray_end_y = self.center  # these will hold the x, y coordinates of the ray's end point
        x_step = self.VISION_STEP * cos(self.angle+additional_angle)
        y_step = self.VISION_STEP * sin(self.angle+additional_angle)
        
        for i in range(self.VISION_RANGE):
            vision_ray_end_x += x_step
            vision_ray_end_y += y_step
            color = screen.get_at((vision_ray_end_x, vision_ray_end_y))
            
            if color in OBSTACLE_COLORS:
                distance = hypot(vision_ray_end_x - self.center[0], vision_ray_end_y - self.center[1])
                self.alive = int(distance) <= self.DEATH_DISTANCE[vision_type]
                return distance
            
        return hypot(vision_ray_end_x - self.center[0], vision_ray_end_y - self.center[1])
        
        # pygame.draw.line(screen, (255, 242, 0), (x_coo, y_coo), 1, 1)
      
    def get_vision_rays_length(self, screen):
        frontal_distance = self.get_distance(screen, "front")
        left_distance = self.get_distance(screen, "left")
        right_distance = self.get_distance(screen, "right")
        diagonal_left_distance = self.get_distance(screen, "front-left")
        diagonal_right_distance = self.get_distance(screen, "front-right")
        return [frontal_distance, left_distance, right_distance, diagonal_left_distance, diagonal_right_distance]
    
    # --------------------------- Update Methods -------------------------------
    def _update_angle(self, dt):  # clockwise: direction=1  | counterclockwise: dir = -1 | no change: dir = 0
        self.angle += self.steering_direction * self.ANGULAR_SPEED * dt  # % 2*pi?

    def _update_speed(self, dt):
        # acceleration: simulating the force applied by the engine to make the car move.
        # when the engine is shut down, the direction is 0 meaning there is no acceleration generated by the engine.
        a = self.engine_force_direction * self.ACCELERATION
    
        # movement direction: 1 -> car going forward; -1 -> car going backwards; 0 -> car not moving
        # This is different from the direction, since it is not related to the engine generating acceleration.
        # As long as the car is moving, the modulo has a non-zero value due to inertia.
        mov_direction = ((self.linear_speed > 0) - (self.linear_speed < 0))
    
        # resistance: sum of forces with opposite direction of the car's movement.
        # It has the opposite direction of the car's movement, because it will be treated as a deceleration
        r = mov_direction * (self.RESISTENCE + self.brake * self.BRAKE_FORCE)
    
        updated_speed = int(self.linear_speed + (a - r) * dt)  # V = V0 + (a - resistance)*t
    
        # guarantees that the speed is between the established limits
        self.linear_speed = min(self.MAX_LINEAR_SPEED, max(-self.MAX_LINEAR_SPEED, updated_speed))
    
    def _update_hit_box(self):
        rect = self.original_image.get_rect(center=self.center)
        pivot = pygame.math.Vector2(self.center)
        angle = -self.angle * 180 / pi
        self.hit_box = [(Vector2(rect.topleft) - pivot).rotate(angle) + pivot,
                        (Vector2(rect.topright) - pivot).rotate(angle) + pivot,
                        (Vector2(rect.bottomright) - pivot).rotate(angle) + pivot,
                        (Vector2(rect.bottomleft) - pivot).rotate(angle) + pivot]
    
    def _update_vision_rays(self):
        pass
    
    def _update_image(self):
        # offset from pivot to center
        image_rect = self.image.get_rect(topleft=(self.x - self.SIZE[0] / 2, self.y - self.SIZE[1] / 2))
        offset_center_to_pivot = pygame.math.Vector2((self.x, self.y)) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)

        # rotated image center
        self.center = (self.x - rotated_offset.x / 2, self.y - rotated_offset.y / 2)

        # get a rotated image
        self.image = pygame.transform.rotate(self.original_image, self.angle * 180 / pi)
        self.rect = self.image.get_rect(center=self.center)
        
    def update(self, dt):
        self._update_angle(dt)
        self._update_speed(dt)
        self.x += self.linear_speed * sin(self.angle) * dt
        self.y += self.linear_speed * cos(self.angle) * dt
        
        self._update_image()
        self._update_hit_box()
        self._update_vision_rays()
    
    # --------------------------- Drawing Methods -------------------------------
    def draw(self, screen):
        # drawing the car's hit-box
        pygame.draw.lines(screen, (255, 255, 0), True, self.hit_box, 1)
        # drawing the car
        screen.blit(self.image, self.rect)
