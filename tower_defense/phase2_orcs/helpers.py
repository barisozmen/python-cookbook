import math
import random

def jitter(*args, amount):
    if len(args) == 1:
        return args[0] + random.randint(-amount, amount)
    else:
        return tuple(x + random.randint(-amount, amount) for x in args)





entity_grid = {}
spatial_grid = {}
GRID_CELL_SIZE = 50


def get_cell_key(x, y):
    """Convert world coordinates to grid cell coordinates"""
    cell_x = x // GRID_CELL_SIZE
    cell_y = y // GRID_CELL_SIZE
    return (cell_x, cell_y)

def record_entity_positions(entities):
    # Clear the spatial grid before repopulating
    spatial_grid.clear()
    
    for entity in entities:
            
        # Store entity position for direct lookup
        entity_grid[entity.id] = (entity.x, entity.y)
        
        # Add entity to spatial grid
        cell_key = get_cell_key(entity.x, entity.y)
        if cell_key not in spatial_grid:
            spatial_grid[cell_key] = []
        spatial_grid[cell_key].append(entity)


def performantly_get_closest_entities(x, y, max_distance):
    closest_entities = []
    closest_distance = float('inf')
    
    # Calculate the range of cells to check based on max_distance
    cell_range = int(max_distance // GRID_CELL_SIZE) + 1
    center_cell = get_cell_key(x, y)
    
    # Only check cells within the max_distance
    for dx in range(-cell_range, cell_range + 1):
        for dy in range(-cell_range, cell_range + 1):
            cell_key = (center_cell[0] + dx, center_cell[1] + dy)
            
            # Skip if this cell doesn't exist in our grid
            if cell_key not in spatial_grid:
                continue
                
            # Check entities in this cell
            for entity in spatial_grid[cell_key]:
                # Calculate actual distance
                dx = entity.x - x
                dy = entity.y - y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance <= max_distance:
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_entities = [entity]
                    elif distance == closest_distance:
                        closest_entities.append(entity)
    
    return closest_entities



def aabb_collision(x,y1,x2,y2):
    return 
