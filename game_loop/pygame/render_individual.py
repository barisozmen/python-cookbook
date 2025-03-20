import time
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load a simple sprite image
sprite_img = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(sprite_img, (255, 0, 0), (16, 16), 16)

# List of sprite positions
sprites = [(random.randint(0, 768), random.randint(0, 568)) for _ in range(100)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # White background
    # Render each sprite individually
    start = time.time()
    for pos in sprites:
        screen.blit(sprite_img, pos)
    end = time.time()
    print(f"Time taken: {end - start} seconds")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()