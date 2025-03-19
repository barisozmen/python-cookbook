import random
import sys
from pathlib import Path
import re
sys.path.append(str(Path(__file__).parent.parent))
from metaclasses import copy_class


map = '''
########################
S000000000000000000000##
#####################0##
###0000000000000000000##
###00###################
###00###################
####0000000000000000000#
######################0#
######################0#
######################0#
G0000000000000000000000#
########################
'''
MAP_GRID_SIZE = 64


TILE_SIZE = (MAP_GRID_SIZE, MAP_GRID_SIZE)

assets_path = Path(__file__).parent / 'assets' 

def load_multiple_images(path):
    directory = assets_path / path
    pattern = re.compile(r'(\d+)\.(png|jpg)$')
    image_files = sorted([f for f in directory.iterdir() if f.is_file() and pattern.search(f.name)], 
                         key=lambda f: int(re.search(r'(\d+)\.(png|jpg)$', f.name).group(1)))
    return [pygame.image.load(str(f)) for f in image_files]

asset_manager = {
    asset_type: load_multiple_images(asset_type) 
    for asset_type in [
        'tile', 'valley', 'spawner', 'gate']}



class Valley:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_key = 'valley'
        self.image_index = random.randint(0, len(asset_manager[self.image_key]) - 1)

class Path:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_key = 'tile'
        self.image_index = random.randint(0, len(asset_manager[self.image_key]) - 1)

class Spawner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_key = 'spawner'
        self.image_index = random.randint(0, len(asset_manager[self.image_key]) - 1)
        
class Gate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_key = 'gate'
        self.image_index = random.randint(0, len(asset_manager[self.image_key]) - 1)


meaning = {
    '#': Valley,
    '0': Path,
    'S': Spawner,
    'G': Gate
}




map_grid = []

for i, row in enumerate([x for x in map.split('\n') if x.strip()]):
    for j, char in enumerate(row):
        map_grid.append(
            meaning[char](i+MAP_GRID_SIZE//2, j+MAP_GRID_SIZE//2)
        )
        
n,m=i+1,j+1


import pygame

pygame.init()




screen = pygame.display.set_mode((m*MAP_GRID_SIZE, n*MAP_GRID_SIZE))
pygame.display.set_caption("Tower Defense Map")

running = True

def get_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update_state():
    pass


def draw_single_grid(i, j, color, screen):
    pygame.draw.rect(screen, color, (j*MAP_GRID_SIZE, i*MAP_GRID_SIZE, MAP_GRID_SIZE, MAP_GRID_SIZE))

def render():
    screen.fill((128, 128, 128))  # Clear screen with gray background
    
    for entity in map_grid:
        if isinstance(entity, Wall):
            draw_single_grid(entity.x-MAP_GRID_SIZE//2, entity.y-MAP_GRID_SIZE//2, entity.color, screen)
        elif isinstance(entity, Path):
            entity.render()
        elif isinstance(entity, Spawner):
            draw_single_grid(entity.x-MAP_GRID_SIZE//2, entity.y-MAP_GRID_SIZE//2, entity.color, screen)
        elif isinstance(entity, Exit):
            draw_single_grid(entity.x, entity.y, entity.color, screen)
    
    pygame.display.flip()  # Update the full display




while running:
    get_input()
    update_state()
    render()
    pygame.time.Clock().tick(60)  # Limit to 60 frames per second

pygame.quit()  # Clean up pygame when done














