import time
import pygame
import math

class GameLoop:
    def __init__(self):
        self.is_running = False
        self.update_rate = 1/60  # 10 updates per second
        self.game_time = 0
        self.last_update_time = 0

        # Initialize Pygame
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Window")
        
        # Add a background color
        self.bg_color = (50, 50, 50)  # Dark gray
        
        # Add a test rectangle for demonstration
        self.rect_x = 400
        self.rect_y = 300
        self.rect_color = (255, 0, 0)  # Red

        # Add player movement variables
        self.player_speed = 1000  # pixels per second
        self.player_dx = 0
        self.player_dy = 0

    def start(self):
        self.is_running = True
        self.last_update_time = time.time()
        self.run()

    def stop(self):
        self.is_running = False
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.stop()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:  self.player_dx = -1
                        case pygame.K_RIGHT: self.player_dx = 1
                        case pygame.K_UP:    self.player_dy = -1
                        case pygame.K_DOWN:  self.player_dy = 1
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_LEFT | pygame.K_RIGHT: self.player_dx = 0
                        case pygame.K_UP | pygame.K_DOWN:    self.player_dy = 0

    def update(self, delta_time):
        self.game_time += delta_time
        
        # Update rectangle position based on input
        self.rect_x += self.player_dx * self.player_speed * delta_time
        self.rect_y += self.player_dy * self.player_speed * delta_time
        
        # Keep rectangle within screen bounds
        self.rect_x = max(25, min(self.rect_x, self.screen_width - 25))
        self.rect_y = max(25, min(self.rect_y, self.screen_height - 25))

    def render(self):
        # Clear the screen
        self.screen.fill(self.bg_color)
        
        # Draw the rectangle
        pygame.draw.rect(self.screen, self.rect_color, 
                        (self.rect_x - 25, self.rect_y - 25, 50, 50))
        
        # Update the display
        pygame.display.flip()

    def run(self):
        while self.is_running:
            current_time = time.time()
            elapsed = current_time - self.last_update_time

            # Handle Pygame events
            self.handle_events()

            if elapsed >= self.update_rate:
                self.update(self.update_rate)
                self.render()  # Add rendering after update
                self.last_update_time = current_time

                # If we're running behind, we don't try to catch up
                if elapsed > self.update_rate * 4:
                    self.last_update_time = current_time

            else:
                time.sleep(self.update_rate/2)

            # Small sleep to prevent CPU from running at 100%
            time.sleep(0.001)

if __name__ == "__main__":
    # Example usage
    game = GameLoop()
    try:
        game.start()
    except KeyboardInterrupt:
        game.stop()
        print("\nGame loop stopped")





