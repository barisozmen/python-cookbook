
from collections import defaultdict
import glob
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from component import *
from command import *

from render_system import *




# def number_of_assets_by_type(type):
#     pattern = str(Standardize.cls_to_asset_dir_path(type) / '[0-9]*.png')
#     return len(glob.glob(pattern))


class Entity:
    """A game entity composed of various components."""
    
    def __init__(self, name):
        self.name = name
        self.id = name + '-' + str(id(self))
        self.components = defaultdict(list)
    
    def add_component(self, component):
        """Add a component to this entity."""
        component_type = type(component)
        self.components[component_type].append(component)
        component.attach(self)
        return component
    
    def remove_component(self, component):
        if component in self.components:
            self.components[component] = []
            component.detach()
        return component
    
    def with_component(self, component):
        self.add_component(component)
        return self

    def get_component(self, component_type):
        """Get a component by its type."""
        return self.components.get(component_type)[0]
    
    def get_components_by_instance(self, type):
        for component_list in self.components.values():
            for component in component_list:
                if isinstance(component, type):
                    yield component
    
    def update(self, delta_time: float):
        for component_list in self.components.values():
            for component in component_list:
                if hasattr(component, 'update'):
                    component.update(delta_time)
                    
    
    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}>'
       
       
class Terrain(Entity):
    def __init__(self, breed, x, y):
        super().__init__('terrain')
        self.breed = breed
        self.geo = self.add_component(SquareGeoComponent(x, y, 0, self.breed.model.image.get_width()))
        self.add_component(RenderImageComponent(self.geo, image=self.breed.model.image))
        
           
    def pos(self):
        geo = self.get_component(SquareGeoComponent)
        return geo.x, geo.y
    
    def width(self):
        geo = self.get_component(SquareGeoComponent)
        return geo.width
    





def is_inside(x, y, geo):
    return geo.x - geo.width//2 <= x <= geo.x + geo.width//2 and geo.y - geo.height//2 <= y <= geo.y + geo.height//2

# See [[State Pattern]] or https://gameprogrammingpatterns.com/state.html for making sense of this
class State:
    def handle_input(self, event): ...
    def update(self, delta_time): ...
    def enter(self, screen): ...
        
class DefaultState(State):
    def handle_input(self, pos, input_type, placement):
        if is_inside(*pos, placement.geo):
            if input_type == 'hover':
                return HoveredState()
            elif input_type == 'click':
                return UIOpenState()
        return None
    
    def handle_click(self, pos, placement):
        if is_inside(*pos, placement.geo):
            return None
        return DefaultState()
    def enter(self, placement): pass
            
class HoveredState(State):
    def handle_input(self, pos, input_type, placement):
        if is_inside(*pos, placement.geo):
            if input_type == 'hover':
                return None
            elif input_type == 'click':
                return UIOpenState()
        return DefaultState()
    
class UIOpenState(State):
    def handle_input(self, pos, input_type, placement):
        if not is_inside(*pos, placement.geo) and input_type == 'click':
            return DefaultState()
    def enter(self, placement): pass
        
        
        
from toolz import partial


class Placement(Terrain):
    def __init__(self, breed, x, y):
        super().__init__(breed, x, y)
        self.state = DefaultState()
        
        self.hovered_image_component = RenderShiningImageComponent(self.geo, image=self.breed.model.hovered_image)
        # self.ui_open_image_component = RenderShiningImageComponent(self.geo, image=self.breed.model.ui_open_image)
        
        MOUSE_MOTION.connect(partial(self.handle_input, input_type='hover'))
        MOUSE_LEFT_CLICK.connect(partial(self.handle_input, input_type='click'))
            
    def handle_input(self, pos, input_type):
        new_state = self.state.handle_input(pos, input_type, self)
        if new_state:
            # print(f"State changed from {self.state} to {new_state} for {self}")
            self.state = new_state
            self.state.enter(self)

            



class TerrainBreed:
    def __init__(self, type, image_index, width=32):
        self.model = TerrainRenderModel(type, image_index, width)
        self.type = type
        
    def produce(self, x, y):
        if self.type == 'placement':
            return Placement(self, x, y)
        else:
            return Terrain(self, x, y)



class Orc(Entity):
    def __init__(self, breed, path, map):
        super().__init__('orc')
        self.breed = breed
        self.path = path
        geo = self.add_component(GeoComponent())
        self.add_component(RenderImageComponent(geo, image=self.breed.model.image))
        self.add_component(OrcAIComponent(path, map))
    
    def teleport(self, x, y):
        self.get_component(GeoComponent).teleport(x, y)

class OrcBreed:
    def __init__(self, type='small', max_health=10, damage=1, speed=100):
        self.type = type
        self.max_health = max_health
        self.damage = damage
        self.speed = speed
        self.width = 32 if type == 'small' else 64 if type == 'medium' else 128
        self.model = OrcRenderModel('small', 1, width=self.width)
        
    def produce(self, path, map):
        return Orc(self, path, map)

class MonitorBreed:
    def __init__(self, type='monitor', max_health=10, damage=1, speed=100):
        self.type = type
        self.max_health = max_health
        self.damage = damage
        self.speed = speed
        self.model = OrcRenderModel(type, 1)
    
    
class HUD(Entity):
    """Heads-Up Display entity to show player stats"""
    def __init__(self, gate_manager, gold_manager):
        super().__init__('hud')
        self.add_component(HUDComponent(gate_manager, gold_manager))
