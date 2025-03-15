from collections.abc import Generator
from enum import Enum, auto
import time
from blinker import Signal # Pub/Sub pattern



        
            
def init():
    ...
    
def handle_events(world):
    ...

def update(world):
    ...

def render(world):
    ...
    
    
    
    
    
    

    
    
    
import pygame
import math

from types import SimpleNamespace
    
    
 
PLAYER = 'player'   
QUIT, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, \
STOP_HORIZONTAL_MOVE, STOP_VERTICAL_MOVE = [Signal() for _ in range(7)]



class Entity: pass 
class PhysicalEntity(Entity):
    def __init__(self, x, y, *args, vx=0, vy=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = SimpleNamespace(x=x, y=y)
        self.velocity = SimpleNamespace(vx=vx, vy=vy)
    
class EntityBoundCommand:
    def __init__(self, entity, *args, signal=None, **kwargs): 
        self.entity = entity
        if signal: 
            self.connect(signal)
    def execute(self): ...
    def connect(self, signal): signal.connect(self.execute)
    
class StartMoveLeft(EntityBoundCommand):
    def execute(self): self.entity.velocity.x = -1
class StartMoveRight(EntityBoundCommand):
    def execute(self): self.entity.velocity.x = 1
class StartMoveUp(EntityBoundCommand):
    def execute(self): self.entity.velocity.y = -1
class StartMoveDown(EntityBoundCommand):
    def execute(self): self.entity.velocity.y = 1
class StopHorizontalMove(EntityBoundCommand):
    def execute(self): self.entity.velocity.x = 0
class StopVerticalMove(EntityBoundCommand):
    def execute(self): self.entity.velocity.y = 0


class Player(PhysicalEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            StartMoveLeft(self, MOVE_LEFT),
            StartMoveRight(self, MOVE_RIGHT),
            StartMoveUp(self, MOVE_UP),
            StartMoveDown(self, MOVE_DOWN),
            StopHorizontalMove(self, STOP_HORIZONTAL_MOVE),
            StopVerticalMove(self, STOP_VERTICAL_MOVE),
        }

    def start_move_left(self): self.velocity.x = -1
    def start_move_right(self): self.velocity.x = 1
    def start_move_up(self): self.velocity.y = -1
    def start_move_down(self): self.velocity.y = 1
    def stop_horizontal_move(self): self.velocity.x = 0
    def stop_vertical_move(self): self.velocity.y = 0

    def update(self, delta_time):
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time


class World:
    def __init__(self):
        self.running = True
        self.time = 0
        self.entities = {
            Player(),
        }
        self.bg_color = 'lightblue'






class ExternalWorldConnection:
    def handle_events(self):
        ...
    def render(self, world):
        ...




class PyGameExternal(ExternalWorldConnection):
    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT: QUIT.send(PLAYER)
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:  MOVE_LEFT.send(PLAYER)
                        case pygame.K_RIGHT: MOVE_RIGHT.send(PLAYER)
                        case pygame.K_UP:    MOVE_UP.send(PLAYER)
                        case pygame.K_DOWN:  MOVE_DOWN.send(PLAYER)
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_LEFT | pygame.K_RIGHT: STOP_HORIZONTAL_MOVE.send(PLAYER)
                        case pygame.K_UP | pygame.K_DOWN:    STOP_VERTICAL_MOVE.send(PLAYER)
    
    def render(self, world):
        self.screen.fill(world.bg_color) # clear the screen
        for entity in world.entities:
            self.screen.blit(entity.image, entity.position) # draw the entity
        pygame.display.flip() # update the screen




def update(world, delta_time):
    for entity in world.entities:
        entity.update(delta_time)


    
def make_iterate(handle_events, update, render):
    def _iterate(world, delta_time):
        handle_events()
        update(world, delta_time)
        render(world)
    return _iterate


def game_loop(init, iterate, fps=60):
    last_update_time = 0
    update_interval = 1.0 / fps
    world = init()
    while world.running:
        elapsed_time = time.time() - last_update_time
        if elapsed_time > update_interval:
            world = iterate(world, elapsed_time)
            last_update_time = time.time()
        time.sleep(update_interval/3) # Small sleep to prevent CPU from running at 100%

game_loop(
    World,
    make_iterate(
        PyGameExternal.handle_events, 
        update, 
        PyGameExternal.render
    ),
    fps=60
)