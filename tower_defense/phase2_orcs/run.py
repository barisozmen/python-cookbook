''' 
Design patterns used:
- Flyweight
- Component
- Singleton
- Factory
'''
from collections import defaultdict
import random
import sys
from pathlib import Path
import glob
import time
from functools import lru_cache
from contextlib import contextmanager

import pygame

from component import *
from render_system import *
from entity import *
from helpers import *
from command import *
from managers import *

sys.path.append(str(Path(__file__).parent.parent)); sys.path.append(str(Path(__file__).parent.parent.parent)) ;sys.path.append(str(Path(__file__).parent.parent.parent.parent))




time_recorder = defaultdict(list)
def time_logger(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        time_recorder[fn.__name__].append(end-start)
        return result
    return wrapper


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
    def __init__(self, fps=60):
        self.entities = []
        self.fps = fps
        self.delta_time = 1.0/fps
        self.render_system = None
        self.input_system = None
        self.running = True
        self.game_over = False
        GAME_OVER.connect(self.on_game_over)
        
    
    def on_game_over(self, *args, **kwargs):
        print("Game over")
        self.game_over = True
    
    def add_entity(self, entity):
        """Add an entity to the game."""
        self.entities.append(entity)
        return entity
    
    @time_logger
    def input(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        MOUSE_LEFT_CLICK.send((mouse_x, mouse_y))
                        
                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        MOUSE_LEFT_RELEASE.send((mouse_x, mouse_y))
                        
                case pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    MOUSE_MOTION.send((mouse_x, mouse_y))
                    
                case pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        GAME_RESTART.send()
    
    @time_logger
    def update(self):
        """Update all entities."""
        for entity in self.entities:
            entity.update(self.delta_time)
    
    @time_logger
    def render(self):
        self.render_system.render(self.entities)
        
        if self.game_over: self.render_system.render_game_over_message("Game Over - Press R to Restart")
        
        self.render_system.flip()
        
    def report(self):
        self.reporter.report()
        
    def loop(self):
        while self.running:
            with reporter():
                self.input()
                if not self.game_over:
                    self.update()
                self.render()
            
            if self.game_over:
                pygame.time.Clock().tick(10)  # Limit to 60 frames per second
            else:
                pygame.time.Clock().tick(self.fps)  # Limit to 60 frames per second
        
        pygame.quit()

class Map:
    num_rows = None
    num_cols = None
    models = None
    symbol_to_class = {
        '#': 'valley', '.': 'road',
        'S': 'spawner','G': 'gate',
        'O': 'placement', '0': 'placement',
    }
    def __init__(self, map, grid_size):
        self.rows = [x for x in map.split('\n') if x.strip()]
        self.num_rows = len(self.rows)
        self.num_cols = len(self.rows[0])
        self.grid_size = grid_size
        self.width = self.num_cols*self.grid_size
        self.height = self.num_rows*self.grid_size
        self.spawners = []
        self.gates = []
        self.flags = {}
    def init_terrain_breeds(self):
        valley_breeds = [TerrainBreed('valley', i) for i in range(1, 3)]
        road_breeds = [TerrainBreed('road', i) for i in range(1, 8)]
        spawner_breeds = [TerrainBreed('spawner', i) for i in range(1, 2)]
        gate_breeds = [TerrainBreed('gate', i) for i in range(1, 2)]
        placement_breeds = [TerrainBreed('placement', i) for i in range(1, 2)]
        self.terrain_breeds = {
            'valley': valley_breeds,
            'road': road_breeds,
            'spawner': spawner_breeds,
            'gate': gate_breeds,
            'placement': placement_breeds,
        }
        
    def resolve_from_grid_index(self, _):
        return _*self.grid_size + (self.grid_size//2)
        
    def generate(self):
        self.init_terrain_breeds()
        for i, row in enumerate(self.rows):
            for j, char in enumerate(row):
                x, y = self.resolve_from_grid_index(j), self.resolve_from_grid_index(i)

                terrain_type = 'road' if char.islower() else self.symbol_to_class[char]
                    
                breed = random.choice(self.terrain_breeds[terrain_type])
                entity = breed.produce(x, y)
                if char.islower():
                    entity.add_component(PathFlagComponent(char))
                    self.flags[char] = entity.pos()
                elif terrain_type == 'spawner':
                    self.spawners.append(entity)
                    self.flags['S'] = entity.pos()
                elif terrain_type == 'gate':
                    self.gates.append(entity)
                    self.flags['G'] = entity.pos()
                yield entity
        
    @property
    def spawner_pos(self, i=0):
        spawner = self.spawners[i]
        geo = spawner.get_component(SquareGeoComponent)
        return geo.x, geo.y
    
    @property
    def gate_pos(self, i=0):
        gate = self.gates[i]
        geo = gate.get_component(SquareGeoComponent)
        return geo.x, geo.y
    


class BottomMenu:
    def __init__(self):
        self.height = 100
        
class UpperMenu:
    def __init__(self):
        self.height = 50
        
        
        
        



ascii_map = '''
##########################
#000000000000000000000####
#000000000000000000000####
S....................a.00#
S....................b.00#
#0000OOOOOOOOOOOOOOOO..00#
#0000OOOOOOOOOOOOOOOO..00#
####e.................c00#
####.f...............d.00#
#00#..000000000000000000##
#00#..000000000000000000##
#00#..000000000000000000##
#00#..####################
#00#g.................j.##
#00#.h.................i##
#0OOOOOOOOOOOOOOOOOOOO..##
##OOOOOOOOOOOOOOOOOOOO..##
##OOOOOOOOOOOOOOOOOOOO..##
##OOOOOOOOOOOOOOOOOOOO..##
##OOOOOOOOOOOOOOOOOOOO..##
G.....................k.##
G......................l##
##########################'''

map = Map(ascii_map, grid_size=32)

bottom_menu = BottomMenu()
upper_menu = UpperMenu()


game = Game(fps=30)
game.render_system = RenderSystem(size=(map.width, map.height+bottom_menu.height+upper_menu.height))



for entity in map.generate():
    game.add_entity(entity)


orc_paths = [
    ['S', 'a', 'c', 'e', 'h','i','k', 'G',],
    ['S', 'a', 'd', 'f', 'g','i','k', 'G',],
    ['S', 'a', 'c', 'e', 'h','i','l', 'G',],
    ['S', 'a', 'c', 'f', 'g','i','k', 'G',],
    ['S', 'b', 'd', 'e', 'g','j','l', 'G',],
    ['S', 'b', 'c', 'e', 'g','j','k', 'G',],
    ['S', 'b', 'd', 'e', 'h','j','l', 'G',],
    ['S', 'b', 'c', 'f', 'h','i','k', 'G',],
    ['S', 'a', 'd', 'f', 'h','i','l', 'G',],
    ['S', 'b', 'c', 'f', 'h','i','k', 'G',],
]



# type object pattern
small_orc_breed = OrcBreed(type='small', max_health=100, damage=1, speed=300)
medium_orc_breed = OrcBreed(type='medium', max_health=500, damage=2, speed=100)
# large_orc_breed = OrcBreed(max_health=30, damage=3, speed=40)

for _ in range(100):
    orc = small_orc_breed.produce(random.choice(orc_paths), map=map)
    orc.teleport(*jitter(*map.spawner_pos, amount=40))
    game.add_entity(orc)
    
for _ in range(10):
    orc = medium_orc_breed.produce(random.choice(orc_paths), map=map)
    orc.teleport(*jitter(*map.spawner_pos, amount=40))
    game.add_entity(orc)



gate_manager = GateManager(game)
gold_manager = GoldManager(game)
orc_manager = OrcManager(game)


game.add_entity(HUD(gate_manager=gate_manager, gold_manager=gold_manager))


game.loop()