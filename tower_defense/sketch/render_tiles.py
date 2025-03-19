import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efficient Rendering of Multiple Images")


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))
print(sys.path)
# Load image once and resize it
original_image = pygame.image.load("game_loop/tower_defense/sketch/assets/tiles/1.png").convert_alpha()
TILE_SIZE = (64, 64)  # Set your desired size here (width, height in pixels)
image = pygame.transform.scale(original_image, TILE_SIZE)  # Resize the image

# Define Sprite Class
class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image  # Reuse the same image
        self.rect = self.image.get_rect(topleft=(x, y))

# Create a sprite group and add multiple instances
sprite_group = pygame.sprite.Group()
positions = [(100, 100), (300, 200), (500, 400), (200, 300), (400, 100)]

for pos in positions:
    sprite_group.add(ImageSprite(*pos))

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))  # Clear screen

    sprite_group.draw(screen)  # Draw all sprites at once (efficient!)

    pygame.display.flip()  # Update display

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
