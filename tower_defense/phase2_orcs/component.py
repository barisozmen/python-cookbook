import math
from functools import lru_cache

import pygame
from helpers import *
from command import *
from blinker import Signal

class Component():
    """Base component class that all components will inherit from."""
    def __init__(self):
        self.entity = None
    def attach(self, entity): self.entity = entity
    def detach(self): self.entity = None
        
    def update(self, delta_time: float): ...

@lru_cache(maxsize=None)
def movement_vector(rotation):
    angle_rad = math.radians(rotation)
    ux = math.cos(angle_rad)
    uy = math.sin(angle_rad)
    return ux, uy


class GeoComponent(Component):
    """Component that handles position, rotation, and scale."""
    
    def __init__(self, x=0, y=0, rotation=0, speed=0):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed  # Single speed value instead of vx/vy
        self.rotation = rotation
    
    def update(self, delta_time: float):
        ux, uy = movement_vector(self.rotation)
        dx = self.speed * ux * delta_time
        dy = self.speed * uy * delta_time
        self.move(dx, dy)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def teleport(self, x, y):
        self.x = x
        self.y = y
    
    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
        
    def set_speed(self, speed):
        self.speed = speed

class SpriteGeoComponent(GeoComponent, pygame.sprite.Sprite): ...

class SquareGeoComponent(GeoComponent):
    def __init__(self, x: float = 0, y: float = 0, rotation: float = 0, width: float = 0):
        super().__init__(x, y, rotation)
        self.width = width
        self.height = width
        
class PathFlagComponent(Component):
    def __init__(self, flag: str):
        super().__init__()
        self.flag = flag
        
        
        
        
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        
class OrcAIComponent(Component):
    def __init__(self, path, map):
        super().__init__()
        self.memory = {}
        self.path = path
        self.map = map
        self.flags_i_have_seen = []
        self.my_target = path[1]
        
    def update(self, delta_time: float):
        my_geo = self.entity.get_component(GeoComponent)
        my_x, my_y = my_geo.x, my_geo.y
        target_x, target_y = self.map.flags[self.my_target]
        if distance(my_x, my_y, target_x, target_y) < 5:
            if self.my_target == 'G':
                
                ORC_REACHES_GATE.send(self.entity)
                
            else:
                self.my_target = self.path[self.path.index(self.my_target) + 1]
        my_geo.rotation = math.degrees(math.atan2(target_y - my_y, target_x - my_x))
        
        my_geo.set_speed(jitter(self.entity.breed.speed, amount=30))

        
        
        