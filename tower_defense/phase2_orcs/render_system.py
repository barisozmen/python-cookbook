from pathlib import Path
import pygame

import sys

sys.path.append(str(Path(__file__).parent.parent)); sys.path.append(str(Path(__file__).parent.parent.parent)) ;sys.path.append(str(Path(__file__).parent.parent.parent.parent))


from metaclasses import SingletonByArgsMetaclass



class Standardize:
    @staticmethod
    def cls_to_asset_dir_path(type):
        return  Path(__file__).parent.parent / 'assets'  / type.lower()
    @staticmethod
    def assets_dir_path():
        return Path(__file__).parent.parent / 'assets'

# def flip(sprites):
#     return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


# def load_sprite_sheets(dir1, dir2, width, height, direction=False):
#     path = Standardize.assets_dir_path() / dir1 / dir2
#     images = [f.name for f in glob.glob(str(path / '*.png'))]

#     all_sprites = {}

#     for image in images:
#         sprite_sheet = pygame.image.load(path / image).convert_alpha()

#         sprites = []
#         for i in range(sprite_sheet.get_width() // width):
#             surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
#             rect = pygame.Rect(i * width, 0, width, height)
#             surface.blit(sprite_sheet, (0, 0), rect)
#             sprites.append(pygame.transform.scale2x(surface))

#         if direction:
#             all_sprites[image.replace(".png", "") + "_right"] = sprites
#             all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
#         else:
#             all_sprites[image.replace(".png", "")] = sprites

#     return all_sprites


class RenderComponent:
    def __init__(self, geo):
        self.entity = None
        self.geo = geo
    def attach(self, entity): self.entity = entity
    def detach(self): self.entity = None

class RenderImageComponent(RenderComponent):
    def __init__(self, geo, image):
        super().__init__(geo)
        self.image = image

        
    def render(self, screen):
        image_width, image_height = self.image.get_width(), self.image.get_height()
        
        if hasattr(self, 'shadow_image'):    
            shadow_width, shadow_height = self.shadow_image.get_width(), self.shadow_image.get_height()
            shadow_offset = (shadow_width - image_width), (shadow_height - image_height)
            
            rotated_shadow_image = pygame.transform.rotate(self.shadow_image, -self.geo.rotation)
            # Get the rect of the rotated image and set its center to match the original center
            shadow_rect = rotated_shadow_image.get_rect(center=(self.geo.x + image_width//2 + shadow_offset[0]//2, 
                                                    self.geo.y + image_height//2 + shadow_offset[1]//2))
            # Draw the rotated image at the adjusted position
            screen.blit(rotated_shadow_image, shadow_rect.topleft)
        
        # MAIN IMAGE
        # Rotate the image based on the geo component's rotation
        rotated_image = pygame.transform.rotate(self.image, -self.geo.rotation)
        # Draw the rotated image at the adjusted position
        screen.blit(rotated_image, (self.geo.x - self.image.get_width()//2, self.geo.y - self.image.get_height()//2))

class RenderShiningImageComponent(RenderComponent):
    def __init__(self, geo, image):
        super().__init__(geo)
        self.image = image

    def render(self, screen):
        screen.blit(self.image, (self.geo.x - self.image.get_width()//2, self.geo.y - self.image.get_height()//2))




class ScreenDebugWrapper:
    def __init__(self, screen):
        self.screen = screen
        
    def blit(self, *args, **kwargs):
        # You can log or monitor blit operations here
        # print(f'screen.blit called with {args} and {kwargs}')
        return self.screen.blit(*args, **kwargs)
    
    def get_width(self):
        return self.screen.get_width()
    
    def get_height(self):
        return self.screen.get_height()
    
    def get_rect(self, *args, **kwargs):
        return self.screen.get_rect(*args, **kwargs)
    
    def fill(self, *args, **kwargs):
        return self.screen.fill(*args, **kwargs)
    
    def get_surface(self):
        return self.screen
    
    def __getattr__(self, attr):
        # Pass through any other attributes/methods to the original screen
        return getattr(self.screen, attr)


class RenderSpriteComponent(RenderComponent):
    def __init__(self, geo, sprite):
        super().__init__(geo)
        self.sprite = sprite

    def render(self, screen):
        screen.blit(self.sprite, (self.geo.x - self.sprite.get_width()//2, self.geo.y - self.sprite.get_height()//2))



class HUDComponent(RenderComponent):
    def __init__(self, gate_manager, gold_manager):
        super().__init__(None)  # HUD doesn't need geo component
        self.gate_manager = gate_manager
        self.gold_manager = gold_manager
        self.font = pygame.font.SysFont('Arial', 24)
        # Load gold icon
        gold_icon_path = Standardize.assets_dir_path() / 'ui' / 'gold_icon.png'
        self.gold_icon = pygame.image.load(gold_icon_path).convert_alpha()
        self.gold_icon = pygame.transform.scale(self.gold_icon, (30, 30))  # Adjust size as needed
        
        # Load heart icon
        heart_icon_path = Standardize.assets_dir_path() / 'ui' / 'heart_icon.png'
        self.heart_icon = pygame.image.load(heart_icon_path).convert_alpha()
        self.heart_icon = pygame.transform.scale(self.heart_icon, (30, 30))  # Adjust size as needed
        
        # Load tower icons
        self.tower_icons = []
        self.tower_names = ["archer", "cannon", "freezer", "magic"]
        self.selected_tower_index = 0  # Track which tower is selected
        
        for tower_name in self.tower_names:
            icon_path = Standardize.assets_dir_path() / 'ui' / f'tower_{tower_name}.png'
            try:
                icon = pygame.image.load(icon_path).convert_alpha()
                icon = pygame.transform.scale(icon, (50, 50))  # Larger size for tower icons
                self.tower_icons.append(icon)
            except pygame.error:
                # Fallback if image doesn't exist
                print(f"Warning: Could not load tower icon: {icon_path}")
                fallback = pygame.Surface((50, 50), pygame.SRCALPHA)
                fallback.fill((100, 100, 100, 200))
                self.tower_icons.append(fallback)
        
    def render(self, screen):
        # Create a semi-transparent background for the HUD
        hud_bg = pygame.Surface((250, 60), pygame.SRCALPHA)  # Wider but shorter for side-by-side layout
        hud_bg.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(hud_bg, (10, 10))
        
        # Render health icon and text
        screen.blit(self.heart_icon, (20, 20))
        health_text = self.font.render(f"{self.gate_manager.home_points}", True, (255, 0, 0))
        screen.blit(health_text, (60, 25))  # Position text next to the heart icon
        
        # Render gold icon and text side by side with health
        screen.blit(self.gold_icon, (120, 20))  # Positioned to the right of health
        gold_text = self.font.render(f"{self.gold_manager.gold}", True, (255, 215, 0))
        screen.blit(gold_text, (160, 25))  # Position text next to the gold icon
        
        # Render tower selection bar at the bottom of the screen
        self.render_tower_selection(screen)
    
    def render_tower_selection(self, screen):
        # Create a semi-transparent background for the tower selection bar
        screen_width = screen.get_width()
        bar_width = 300  # Width of the tower selection bar
        bar_height = 70  # Height of the tower selection bar
        
        # Center the bar at the bottom of the screen
        bar_x = (screen_width - bar_width) // 2
        bar_y = screen.get_height() - bar_height - 10  # 10px padding from bottom
        
        # Draw the background
        tower_bar_bg = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        tower_bar_bg.fill((0, 0, 0, 150))  # Black with opacity
        screen.blit(tower_bar_bg, (bar_x, bar_y))
        
        # Draw the tower icons
        icon_spacing = bar_width // len(self.tower_icons)
        for i, icon in enumerate(self.tower_icons):
            icon_x = bar_x + i * icon_spacing + (icon_spacing - icon.get_width()) // 2
            icon_y = bar_y + (bar_height - icon.get_height()) // 2
            
            # Draw selection highlight for the selected tower
            if i == self.selected_tower_index:
                highlight_rect = pygame.Rect(icon_x - 5, icon_y - 5, 
                                           icon.get_width() + 10, icon.get_height() + 10)
                # Get the actual pygame Surface if we're dealing with a wrapper
                actual_surface = getattr(screen, 'screen', screen)
                pygame.draw.rect(actual_surface, (255, 215, 0), highlight_rect, 3)  # Gold highlight
            
            screen.blit(icon, (icon_x, icon_y))
    
    def select_next_tower(self):
        self.selected_tower_index = (self.selected_tower_index + 1) % len(self.tower_icons)
    
    def select_previous_tower(self):
        self.selected_tower_index = (self.selected_tower_index - 1) % len(self.tower_icons)
    
    def get_selected_tower_type(self):
        return self.tower_names[self.selected_tower_index]


class RenderSystem:
    def __init__(self, size):
        pygame.init()
        
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Tower Defense Map")
        self.screen.fill((255, 255, 255))
        self.screen = ScreenDebugWrapper(self.screen)  # Wrap the screen object

    def render(self, entities):
        
        terrains = list(filter(lambda e: e.__class__.__name__ == 'Terrain', entities))
        placements = list(filter(lambda e: e.__class__.__name__ == 'Placement', entities))
        orcs = list(filter(lambda e: e.__class__.__name__ == 'Orc', entities))
        hud = next(filter(lambda e: e.__class__.__name__ == 'HUD', entities), None)
        
        # first render terrains
        for terrain in terrains + placements:
            for component in terrain.get_components_by_instance(RenderImageComponent):
                component.render(self.screen)
                pass
        
        # for hovered placements, render the shining image
        for placement in placements:
            if placement.state.__class__.__name__ == 'HoveredState':
                placement.hovered_image_component.render(self.screen)
        
        # then render orcs (they'll be rendered on top of terrains, because they're rendered later)
        for orc in orcs:
            orc.get_component(RenderImageComponent).render(self.screen)
        
        # finally render HUD (on top of everything)
        if hud:
            hud.get_component(HUDComponent).render(self.screen)
        
    def render_game_over_message(self, message):
        font = pygame.font.SysFont('Arial', 48)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(text, text_rect)
        
    def flip(self):
        # if no flip, the screen will be empty
        pygame.display.flip()
        

def apply_muted_effect(image, alpha=220):
    image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    return image
def desaturate_image(image):
    """ Convert a Pygame image to grayscale while keeping transparency. """
    # Convert image to grayscale
    grayscale = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            color = image.get_at((x, y))
            gray = int(0.3 * color.r + 0.59 * color.g + 0.11 * color.b)  # Luminance formula
            grayscale.set_at((x, y), (gray, gray, gray, color.a))  # Preserve alpha
    return grayscale


''' flyweight pattern
models
'''

class TerrainRenderModel(metaclass=SingletonByArgsMetaclass):
    def __init__(self, type, image_index, width=32):
        self.type = type
        self.image_index = image_index
        original_image = pygame.image.load(Standardize.assets_dir_path() / 'terrain' / type.lower() / f'{image_index}.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (width, width))
        
        hovered_image = pygame.image.load(Standardize.assets_dir_path() / 'effects/shining.png').convert_alpha()
        self.hovered_image = pygame.transform.scale(hovered_image, (width, width))
        
        # self.image = desaturate_image(self.image)
        # Apply blur effect to terrain
        
        # Adjust opacity (higher than before but still somewhat transparent)
        # self.image.set_alpha(64)
        
        # Optional: Slightly desaturate the terrain to make orcs pop more
        # self.desaturate(0.1)
    
    def desaturate(self, amount=0.5):
        """Reduce color saturation of the image by converting partially to grayscale"""
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                r, g, b, a = self.image.get_at((x, y))
                # Simple grayscale conversion
                gray = (r + g + b) // 3
                # Blend between original and gray based on amount
                r = int(r * (1 - amount) + gray * amount)
                g = int(g * (1 - amount) + gray * amount)
                b = int(b * (1 - amount) + gray * amount)
                self.image.set_at((x, y), (r, g, b, a))
        
        
def make_shadow_image(image):
    # Create a slightly larger surface for the shadow (wider and shorter)
    scale_width = 1.2  # 20% wider
    scale_height = 0.8  # 20% shorter
    shadow_width = int(image.get_width() * scale_width)
    shadow_height = int(image.get_height() * scale_height)
    
    # Create a new surface for the shadow with the adjusted dimensions
    shadow_image = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    
    # Scale the original image to the new dimensions
    scaled_image = pygame.transform.scale(image, (shadow_width, shadow_height))
    
    # Apply the shadow color
    shadow_color = (50, 50, 50, 128)  # Dark gray with 50% opacity
    shadow_image.blit(scaled_image, (0, 0))
    shadow_image.fill(shadow_color, special_flags=pygame.BLEND_RGBA_MULT)
    
    # Return the shadow image and the calculated offset
    return shadow_image
        
class OrcRenderModel(metaclass=SingletonByArgsMetaclass):
    def __init__(self, type, image_index, width=32):
        self.type = type
        self.image_index = image_index
        original_image = pygame.image.load(Standardize.assets_dir_path() / f'units/orc_{type.lower()}/{image_index}.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (width, width))

        # Create shadow by tinting a copy of the sprite
        self.shadow_image = make_shadow_image(self.image)



