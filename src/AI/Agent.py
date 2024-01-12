import neat.nn
import math
from src.GameEntities.Car import Car


class Agent:
    MAX_TIME_ALIVE = 150  # seconds
    TIME_VALUE = 50 / MAX_TIME_ALIVE  # [goal-dist-points(pts)]/[goal-time(sec)]= (pts/sec)
    PARTS_VALUE = 50 / 60  # [goal-part-points(pts)]/[goal-parts(part)] = (pts/part
    
    def __init__(self, g, nn, avatar):
        self.genome = g  # genome of the agent
        self.genome.fitness = 0
        self.neural_network: neat.nn.FeedForwardNetwork = nn  # neural network that defines the agent's behaviour
        self.Car: Car = avatar  # the class that performs actions in the environment
        self.parts_collected = 0
        self.time_alive = 0
        self.steady = 0  # times the agent chose not to move
    
    @staticmethod
    def normalize(max_value, min_value, value):
        return (value - min_value) / (max_value - min_value)

    @staticmethod
    def activation_function(value):
        return 1 / (1 + math.e ** (-value))

    @staticmethod
    def make_discrete(value):
        if -0.7 <= value <= 0.7:  # comes first because it is the most likely
            return 0
        elif -1 <= value <= -0.7:
            return -1
        return 1
    
    def get_nn_inputs(self):
        # [x, y, speed, angle, vision_ray_length_1, vision_ray_length_2, ...]
        return [self.Car.x, self.Car.y, self.Car.linear_speed, self.Car.angle] + self.Car.get_vision_rays_length()
    
    def move_car(self, movement_directives: [int], dt: float):
        # first directive indicates what acceleration the engine generates: 1-> forward; 0-> none; -1-> backward
        self.Car.activate_speeding(movement_directives[0])
        
        # second directive indicates if brakes should be used: 1-> yes; 0-> no
        self.Car.activate_brakes(movement_directives[1])
        
        # third directive indicates steering behaviour: 1-> left; 0-> none; -1-> right
        self.Car.activate_steering(movement_directives[2])
        
        self.Car.update(dt)
    
    def move(self, dt):
        nn_input = self.get_nn_inputs()
        # 3 possible values instead of infinite
        output = [self.make_discrete(i) for i in self.neural_network.activate(nn_input)]  # careful about format
        self.move_car(output, dt)  # makes the Agent move based on the Neural network output
        self.time_alive += dt

    def update_fitness(self):
        distance_contribute = self.time_alive*self.TIME_VALUE  # goal : 45000 pixels | total: 50 points  |
        parts_contribute = self.parts_collected*self.PARTS_VALUE  # goal: 2.5 pts/part | total: 50 points  |
        # steady_contribute = self.steady*STEADY_W
        self.genome.fitness = parts_contribute+distance_contribute  # +steady_contribute
        if self.genome.fitness >= 10:
            print(f"Fitness = {self.genome.fitness}"
                  f" p={self.parts_collected} -> pc: {parts_contribute} |"
                  f" t={self.time_alive} -> tc: {distance_contribute}")
