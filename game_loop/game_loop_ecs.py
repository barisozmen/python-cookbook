import pygame
from blinker import Signal
import time

# ---------------------- SIGNALS ----------------------
QUIT, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, \
STOP_HORIZONTAL_MOVE, STOP_VERTICAL_MOVE = [Signal() for _ in range(7)]

game_running = True
QUIT.connect(lambda x: globals().update(game_running=False))





# ---------------------- COMMANDS ----------------------

class ComponentBoundCommand:
    def __init__(self, component, *args, signal=None, **kwargs): 
        self.component = component
        if signal: 
            self.connect(signal)
    def execute(self): ...
    def connect(self, signal): signal.connect(self.execute)
    
class StartMoveLeft(ComponentBoundCommand):
    def execute(self): self.component.vx = -1
class StartMoveRight(ComponentBoundCommand):
    def execute(self): self.component.vx = 1
class StartMoveUp(ComponentBoundCommand):
    def execute(self): self.component.vy = -1
class StartMoveDown(ComponentBoundCommand):
    def execute(self): self.component.vy = 1
class StopHorizontalMove(ComponentBoundCommand):
    def execute(self): self.component.vx = 0
class StopVerticalMove(ComponentBoundCommand):
    def execute(self): self.component.vy = 0
    
    
    
# ---------------------- COMPONENTS ----------------------

from types import SimpleNamespace

class Component:
    pass

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, vx=0, vy=0):
        self.vx = vx
        self.vy = vy

class Renderable(Component):
    def __init__(self, color=(255, 0, 0), width=50, height=50):
        self.color = color
        self.width = width
        self.height = height

class PlayerControlsVelocity(Component):
    def __init__(self):
        vel = self.get_component(Velocity)
        self.commands = {
            StartMoveLeft(vel, MOVE_LEFT),
            StartMoveRight(vel, MOVE_RIGHT),
            StartMoveUp(vel, MOVE_UP),
            StartMoveDown(vel, MOVE_DOWN),
            StopHorizontalMove(vel, STOP_HORIZONTAL_MOVE),
            StopVerticalMove(vel, STOP_VERTICAL_MOVE),
        }



# ---------------------- ENTITIES ----------------------
class Entity:
    _next_id = 0
    
    def __init__(self):
        self.id = Entity._next_id
        Entity._next_id += 1
        self.components = {}
        
    def with_components(self, *components):
        for component in components:
            self.add_component(component)
        return self
    
    def add_component(self, component):
        self.components[type(component)] = component
        
    def get_component(self, component_type):
        return self.components.get(component_type)
    
    def has_component(self, component_type):
        return component_type in self.components
    
    
class World:
    def __init__(self):
        ...
    
    
# ---------------------- SYSTEMS ----------------------
import pygame

class System:
    def iterate(self, *args, **kwargs): ...
    
class MovementSystem(System):
    @staticmethod
    def update(world, delta_time):
        for entity in world.entities:
            if entity.has_component(Position) and entity.has_component(Velocity):
                pos = entity.get_component(Position)
                vel = entity.get_component(Velocity)
                pos.x += vel.vx * delta_time
                pos.y += vel.vy * delta_time


class PyGameRenderSystem(System):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("ECS Game")
        self.bg_color = 'lightblue'
        
    def update(self, entities):
        self.screen.fill(self.bg_color)
        for entity in entities:
            if entity.has_component(Position) and entity.has_component(Renderable):
                pos = entity.get_component(Position)
                render = entity.get_component(Renderable)
                pygame.draw.rect(
                    self.screen,
                    render.color,
                    (pos.x - render.width/2, pos.y - render.height/2, 
                     render.width, render.height)
                )
        pygame.display.flip()


class PyGameInputSystem(System):
    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT: 
                    QUIT.send()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:  MOVE_LEFT.send()
                        case pygame.K_RIGHT: MOVE_RIGHT.send()
                        case pygame.K_UP:    MOVE_UP.send()
                        case pygame.K_DOWN:  MOVE_DOWN.send()
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_LEFT | pygame.K_RIGHT: 
                            STOP_HORIZONTAL_MOVE.send()
                        case pygame.K_UP | pygame.K_DOWN:    
                            STOP_VERTICAL_MOVE.send()
    
    
# ---------------------- GAME ----------------------
    
class Game:
    def __init__(self, *args):
        self.entities = set(); self.systems = []
        for arg in args:
            match arg:
                case Entity(): self.add_entity(arg)
                case System(): self.add_system(arg)
                case _: raise ValueError(f"Invalid argument: {arg}")
                
    def iterate(self):
        for system in self.systems:
            system.iterate(self)
    
    def add_entity(self, entity): self.entities.add(entity)
    def add_system(self, system): self.systems.append(system)

# ---------------------- GAME LOOP ----------------------
class BasicLoop:
    def __init__(self, fps=60):
        self.fps = fps
        self.update_interval = 1.0 / fps
        self.last_update_time = 0
        
    def loop(self, *args, **kwargs):
        while game_running:
            elapsed_time = (current_time:= time.time()) - self.last_update_time
    
            if elapsed_time > self.update_interval:
                self.iterate()
                self.last_update_time = current_time
                
            time.sleep(self.update_interval/3)
        

class BasicGame(Game, BasicLoop): ...


simple_game = BasicGame(
    World(), 
    Entity().with_components(
        Position(x=400, y=300), Renderable(),
        Velocity(), PlayerControlsVelocity(), 
    ),
    PyGameInputSystem(), MovementSystem(), PyGameRenderSystem()
)





if __name__ == "__main__":
    simple_game.loop()