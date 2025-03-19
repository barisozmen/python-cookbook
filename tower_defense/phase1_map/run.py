''' 
Design patterns used:
- Flyweight
- Component
- Singleton
- Factory
'''


from ast import Dict
from collections import defaultdict
import random
import sys
from pathlib import Path
import re
import glob
import time
from typing import List

import pygame


sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from metaclasses import SingletonMetaclass


class Standardize:
    @staticmethod
    def cls_to_asset_dir_path(cls):
        return  Path(__file__).parent.parent / 'assets'  / cls.__name__.lower()


def number_of_assets_by_type(type):
    pattern = str(Standardize.cls_to_asset_dir_path(type) / '[0-9]*.png')
    return len(glob.glob(pattern))

class Component:
    """Base component class that all components will inherit from."""
    def __init__(self):
        self.entity = None
        
    def attach(self, entity):
        self.entity = entity
        
    def update(self, delta_time: float): ...

class GeoComponent(Component):
    """Component that handles position, rotation, and scale."""
    
    def __init__(self, x, y, rotation= 0, unit_speed_ppx= 300, vx= 0, vy= 0):
        super().__init__()
        self.x = x
        self.y = y
        self.unit_speed_ppx = unit_speed_ppx
        self.vx = vx
        self.vy = vy
        self.rotation = rotation
    
    def update(self, delta_time: float):
        self.x += self.vx * self.unit_speed_ppx * delta_time
        self.y += self.vy * self.unit_speed_ppx * delta_time
    
    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
    
    def rotate(self, angle: float):
        self.rotation += angle

class SquareGeoComponent(GeoComponent):
    def __init__(self, x: float = 0, y: float = 0, rotation: float = 0, width: float = 0):
        super().__init__(x, y, rotation)
        self.width = width
        self.height = width

class TerrainModel:
    def __init__(self, type, image_index, width):
        self.type = type
        self.image_index = image_index
        original_image = pygame.image.load(Standardize.cls_to_asset_dir_path(type) / f'{image_index}.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (width, width))


class FlyweightFactory(metaclass=SingletonMetaclass):
    def __init__(self):
        self.flyweights = {}

    def get_terrain_model(self, terrain_type, image_index, width):
        key = (terrain_type, image_index)
        if key not in self.flyweights:
            self.flyweights[key] = TerrainModel(terrain_type, image_index, width)
        return self.flyweights[key]
    
    def get_terrain_model_list(self, terrain_type, width):
        n = number_of_assets_by_type(terrain_type)
        print(f'{terrain_type} has {n} assets')
        return [self.get_terrain_model(terrain_type, i, width) for i in range(1, n+1)]


class Entity:
    """A game entity composed of various components."""
    
    def __init__(self, name: str):
        self.name = name
        self.components: Dict[type, Component] = {}
    
    def add_component(self, component: Component):
        """Add a component to this entity."""
        component_type = type(component)
        self.components[component_type] = component
        component.attach(self)
        return component
    
    def get_component(self, component_type: type) -> Component:
        """Get a component by its type."""
        return self.components.get(component_type)
    
    def get_components_by_instance(self, type):
        for component in self.components.values():
            if isinstance(component, type):
                yield component
    
    def update(self, delta_time: float):
        for component in self.components.values():
            component.update(delta_time)
            

class MapEntity(Entity):
    def __init__(self, model, x, y):
        super().__init__('map_entity')
        self.model = model
        geo = self.add_component(SquareGeoComponent(x, y, 0, model.image.get_width()))
        self.add_component(RenderImageComponent(geo, image=model.image))
        
    def render(self):
        self.model.render(self.geo)

class Valley(MapEntity): ...
class Road(MapEntity): ...
class Spawner(MapEntity): ...
class Gate(MapEntity): ...


class RenderComponent(Component):
    def __init__(self, geo):
        super().__init__()
        self.geo = geo

class RenderImageComponent(RenderComponent):
    def __init__(self, geo, image):
        super().__init__(geo)
        self.image = image

    def render(self, screen):
        if self.geo.rotation != 0:
            # Rotate the image based on the geo component's rotation
            rotated_image = pygame.transform.rotate(self.image, -self.geo.rotation)
            # Get the rect of the rotated image and set its center to match the original center
            rect = rotated_image.get_rect(center=(self.geo.x + self.image.get_width()//2, 
                                                 self.geo.y + self.image.get_height()//2))
            # Draw the rotated image at the adjusted position
            screen.blit(rotated_image, rect.topleft)
        else:
            # If no rotation, render normally
            screen.blit(self.image, (self.geo.x - self.image.get_width()//2, self.geo.y - self.image.get_height()//2))

class ScreenDebugWrapper:
    def __init__(self, screen):
        self.screen = screen
        
    def blit(self, *args, **kwargs):
        # You can log or monitor blit operations here
        # print(f'screen.blit called with {args} and {kwargs}')
        return self.screen.blit(*args, **kwargs)
    
    def __getattr__(self, attr):
        # Pass through any other attributes/methods to the original screen
        return getattr(self.screen, attr)

class RenderSystem:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Tower Defense Map")
        self.screen.fill((128, 128, 128))
        self.screen = ScreenDebugWrapper(self.screen)  # Wrap the screen object

    def render(self, entities):
        for entity in entities:
            for component in entity.get_components_by_instance(RenderComponent):
                component.render(self.screen)
        pygame.display.flip()


time_recorder = defaultdict(list)
def time_logger(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        time_recorder[fn.__name__].append(end-start)
        return result
    return wrapper


from contextlib import contextmanager

@contextmanager
def reporter():
    # Access the counter as a nonlocal variable
    if not hasattr(reporter, 'counter'):
        reporter.counter = 0
    
    start = time.time()
    yield
    end = time.time()
    time_recorder['full_loop'].append(end-start)
    
    # Increment counter after each yield
    reporter.counter += 1
    
    if reporter.counter % 100 == 0:
        print(f"\n{reporter.counter} frames.")
        print("Running time averages:")
        for key in time_recorder:
            avg_time = sum(time_recorder[key])/len(time_recorder[key])
            print(f"- {key}: {avg_time}")
        time_recorder.clear()
        

class Game:
    def __init__(self, render_system, fps=60):
        self.entities: List[Entity] = []
        self.fps = fps
        self.delta_time = 1.0/fps
        self.render_system = render_system
        self.running = True
    
    def add_entity(self, entity: Entity):
        """Add an entity to the game."""
        self.entities.append(entity)
        return entity
    
    @time_logger
    def input(self):
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    @time_logger
    def update(self):
        """Update all entities."""
        for entity in self.entities:
            entity.update(self.delta_time)
    
    @time_logger
    def render(self):
        self.render_system.render(self.entities)
        
    def report(self):
        self.reporter.report()
        
    def loop(self):
        while self.running:
            with reporter():
                self.input()
                self.update()
                self.render()
            pygame.time.Clock().tick(self.fps)  # Limit to 60 frames per second
        pygame.quit()

class Map:
    num_rows = None
    num_cols = None
    models = None
    symbol_to_class = {
        '#': Valley, '.': Road,
        'S': Spawner,'G': Gate
    }
    def __init__(self, map, grid_size):
        self.rows = [x for x in map.split('\n') if x.strip()]
        self.num_rows = len(self.rows)
        self.num_cols = len(self.rows[0])
        self.grid_size = grid_size
        self.width = self.num_cols*self.grid_size
        self.height = self.num_rows*self.grid_size
        
    def init_models(self):
        self.models = {cls: FlyweightFactory().get_terrain_model_list(terrain_type=cls, width=self.grid_size) 
                        for cls in self.symbol_to_class.values()}
        
    def resolve_from_grid_index(self, _):
        return _*self.grid_size + (self.grid_size//2)
        
    def generate(self):
        self.init_models()
        for i, row in enumerate(self.rows):
            for j, char in enumerate(row):
                x, y = self.resolve_from_grid_index(j), self.resolve_from_grid_index(i)

                cls = self.symbol_to_class[char]
                assert issubclass(cls, MapEntity)
                model = random.choice(self.models[cls])
                yield cls(model, x, y)
        
ascii_map = '''
##########################
##########################
SS.....................###
SS.....................###
#####################..###
#####################..###
####...................###
####...................###
####..####################
####..####################
####..####################
####..####################
####....................##
####....................##
######################..##
######################..##
######################..##
######################..##
######################..##
GG......................##
GG......................##
##########################'''

map = Map(ascii_map, grid_size=32)

render_system = RenderSystem(size=(map.width, map.height))
game = Game(render_system)

for entity in map.generate():
    game.add_entity(entity)

game.loop()










