import time
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Define a Sprite subclass
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create the image only once and share it among instances
        if not hasattr(GameSprite, 'shared_image'):
            GameSprite.shared_image = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(GameSprite.shared_image, (255, 0, 0), (16, 16), 16)
        self.image = GameSprite.shared_image
        self.rect = self.image.get_rect(topleft=(x, y))

# Create a group of sprites
sprite_group = pygame.sprite.Group()
# Pre-allocate sprites in a single batch
sprites = [GameSprite(random.randint(0, 768), random.randint(0, 568)) for _ in range(1000)]
sprite_group.add(sprites)

# For performance measurement
frame_times = []
max_frames = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # White background
    
    # Render all sprites in one call
    start = time.time()
    sprite_group.draw(screen)
    end = time.time()
    
    frame_time = end - start
    frame_times.append(frame_time)
    if len(frame_times) <= max_frames:
        print(f"Frame {len(frame_times)}: {frame_time:.6f} seconds")
    elif len(frame_times) == max_frames + 1:
        avg_time = sum(frame_times) / len(frame_times)
        print(f"\nAverage rendering time: {avg_time:.6f} seconds")
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()