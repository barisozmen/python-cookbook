'''
Design patterns used:
- ECS (Entity Component System)
- Game loop
- Command pattern
- Signal pattern
- Observer pattern [not sure if used]
- Flyweight pattern [todo]
- State pattern [todo]
'''


from abc import ABCMeta
import pygame
from blinker import Signal
import time



# ---------------------- SIGNALS ----------------------
class DebugSignal(Signal):
    def __init__(self, name=None):
        super().__init__(name)
        self.name = name or f"Signal-{id(self)}"
    def send(self, *args, **kwargs):
        print(f"Signal '{self.name}' was sent with args={args}, kwargs={kwargs}")
        return super().send(*args, **kwargs)



QUIT, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, \
STOP_HORIZONTAL_MOVE, STOP_VERTICAL_MOVE = [DebugSignal() for _ in range(7)]

# Add new mouse signals
MOUSE_LEFT_CLICK, MOUSE_LEFT_RELEASE, MOUSE_MOTION, MOUSE_DRAG = [DebugSignal() for _ in range(4)]

CHANGE_UPDATE_INTERVAL = DebugSignal()


# ---------------------- COMMANDS ----------------------

class Command:
    def __init__(self, obj, *signals, **kwargs):
        self.obj = obj
        if signals: self.connect(signals)
    def do(self, *args, **kwargs): ...
    def undo(self, *args, **kwargs): ...
    def connect(self, signals):
        for signal in signals:
            signal.connect(self.do)
    
class StartMoveLeft(Command):
    def do(self, *args, **kwargs): self.obj.vx = -1
class StartMoveRight(Command):
    def do(self, *args, **kwargs): self.obj.vx = 1
class StartMoveUp(Command):
    def do(self, *args, **kwargs): self.obj.vy = -1
class StartMoveDown(Command):
    def do(self, *args, **kwargs): self.obj.vy = 1
class StopHorizontalMove(Command):
    def do(self, *args, **kwargs): self.obj.vx = 0
class StopVerticalMove(Command):
    def do(self, *args, **kwargs): self.obj.vy = 0
class QuitCommand(Command):
    def do(self, *args, **kwargs): self.obj.running = False


# ---------------------- MIXINS ----------------------

class Mixin:
    def __init__(self, *args, **kwargs):
        pass

class ComponentsMixin(Mixin):
    def __init__(self, *args, **kwargs):
        self.components = {}
        super().__init__(*args, **kwargs)
    def with_components(self, *components):
        for component in components: self.add_component(component)
        return self
    def add_component(self, component): self.components[type(component)] = component
    def get_component(self, component_type): return self.components.get(component_type, None)
    def get_components(self, *component_types): return (self.get_component(component_type) for component_type in component_types)
    def has_component(self, component_type): return component_type in self.components

class CommandsMixin(Mixin):
    def __init__(self, *args, **kwargs):
        self.commands = {}
        super().__init__(*args, **kwargs)
    def with_commands(self, *commands):
        for command in commands: self.add_command(command)
        return self
    def add_command(self, command): self.commands[type(command)] = command
    def get_command(self, command_type): return self.commands.get(command_type, None)
    def get_commands(self, *command_types): return (self.get_command(command_type) for command_type in command_types)
    def has_command(self, command_type): return command_type in self.commands

# ---------------------- COMPONENTS ----------------------
class Component: ...

class Position(Component):
    def __init__(self, x=0, y=0, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Velocity(Component):
    def __init__(self, vx=0, vy=0, unit_pixels_per_second=500):
        self.vx = vx
        self.vy = vy
        self.unit_pixels_per_second = unit_pixels_per_second
        super().__init__()
    def unit_delta_x(self, delta_time): return self.vx * self.unit_pixels_per_second * delta_time
    def unit_delta_y(self, delta_time): return self.vy * self.unit_pixels_per_second * delta_time
    def move_by_unit_delta(self, pos, delta_time):
        pos.x += self.unit_delta_x(delta_time)
        pos.y += self.unit_delta_y(delta_time)
        return pos
    def unmove_by_unit_delta(self, pos, delta_time):
        pos.x -= self.unit_delta_x(delta_time)
        pos.y -= self.unit_delta_y(delta_time)
        return pos

class PlayerControlsVelocity(Component):
    def __init__(self, vel):
        self.commands = {
            StartMoveLeft(vel, MOVE_LEFT),
            StartMoveRight(vel, MOVE_RIGHT),
            StartMoveUp(vel, MOVE_UP),
            StartMoveDown(vel, MOVE_DOWN),
            StopHorizontalMove(vel, STOP_HORIZONTAL_MOVE),
            StopVerticalMove(vel, STOP_VERTICAL_MOVE),
        }

class Renderable(Component):
    def __init__(self, pos=None, color=(255, 0, 0)):
        self.pos = pos
        self.color = color
        self.width = pos.width
        self.height = pos.height

class HasNeighbors(Component):
    def __init__(self, *entities):
        for entity in self.entities:
            match entity:
                case Entity(): self.entities.add(entity)
                case _: raise ValueError(f"Invalid argument: {entity}")



# ---------------------- ENTITIES ----------------------

class Entity(ComponentsMixin, CommandsMixin):
    _next_id = 0
    def __init__(self, *args, id=None, **kwargs):
        self.id = id or Entity._next_id
        Entity._next_id += 1
        super().__init__(*args, **kwargs)
        for arg in args:
            match arg:
                case Component(): self.add_component(arg)
                case Command(): self.add_command(arg)
                case _: raise ValueError(f"Invalid argument: {arg}")

    
class World(Entity): pass

    
# ---------------------- SYSTEMS ----------------------
import pygame

class System:
    def iterate(self, *args, **kwargs): ...
    
class MovementSystem(System):
    @staticmethod
    def iterate(game, delta_time):
        for entity in game.entities:
            pos, vel = entity.get_components(Position, Velocity)
            if pos and vel:
                vel.move_by_unit_delta(pos, delta_time)

class PyGameRenderSystem(System):
    def __init__(self, bg_color='lightblue', screen_size=(800, 600)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("ECS Game")
        self.bg_color = bg_color
        
    def iterate(self, game, delta_time):
        self.screen.fill(self.bg_color)
        for entity in game.entities:
            pos, render = entity.get_components(Position, Renderable)
            if pos and render:
                pygame.draw.rect(
                    self.screen,
                    render.color,
                    (pos.x - render.width/2, pos.y - render.height/2, 
                     render.width, render.height)
                )

class PygameDisplayFlipSystem(System):
    def iterate(self, game, delta_time):
        pygame.display.flip()


class PyGameInputSystem(System):
    def __init__(self):
        self.dragging = False
    def iterate(self, game, delta_time):
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
                        case pygame.K_LEFT | pygame.K_RIGHT: STOP_HORIZONTAL_MOVE.send()
                        case pygame.K_UP | pygame.K_DOWN:    STOP_VERTICAL_MOVE.send()
                # mouse events
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # 1 is left mouse button
                        self.dragging = True
                        MOUSE_LEFT_CLICK.send(pos=event.pos)
                case pygame.MOUSEBUTTONUP:
                    if event.button == 1: # 1 is left mouse button
                        if self.dragging:
                            self.dragging = False
                        MOUSE_LEFT_RELEASE.send(pos=event.pos)
                case pygame.MOUSEMOTION:
                    MOUSE_MOTION.send(pos=event.pos)
                    if self.dragging:
                        MOUSE_DRAG.send(pos=event.pos)
            
    
# ---------------------- GAME ----------------------
class Game(ComponentsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entities = set(); self.systems = []
        self.running = True
        self.commands = {QuitCommand(self, QUIT),}
        for arg in args:
            match arg:
                case Entity(): self.add_entity(arg)
                case System(): self.add_system(arg)
                case Component(): self.add_component(arg)
                case _: raise ValueError(f"Invalid argument: {arg}")
                
    def iterate(self, delta_time):
        for system in self.systems:
            system.iterate(self, delta_time)
    
    def add_entity(self, entity): self.entities.add(entity)
    def get_entity(self, id): return next((entity for entity in self.entities if entity.id == id), None)
    def add_system(self, system): self.systems.append(system)
    def add_commands(self, *commands):
        for command in commands: self.commands[type(command)] = command


# ---------------------- GAME LOOP ----------------------
class BasicLoop:
    def __init__(self, *args, update_interval=(1.0/60), **kwargs):
        self.update_interval = update_interval
        self.last_update_time = 0
        
    def loop(self, *args, **kwargs):
        while self.running:
            elapsed_time = (current_time:= time.time()) - self.last_update_time
    
            if elapsed_time > self.update_interval and self.update_interval>0:
                self.iterate(elapsed_time)
                self.last_update_time = current_time
                
            time.sleep(self.update_interval/3)
        

class BasicGame(Game, BasicLoop):
    def __init__(self, *args, **kwargs):
        BasicLoop.__init__(self, *args, **kwargs)
        Game.__init__(self, *args, **kwargs)