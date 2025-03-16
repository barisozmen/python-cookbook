import itertools
from base import *
import math


# Special signals
HALLOWEEN_BUTTON_CLICK = DebugSignal()


def within_grid(pos, grid_pos):
    x, y = pos
    gx, gy = grid_pos.x, grid_pos.y
    gw, gh = grid_pos.width, grid_pos.height
    return (
        gx - gw/2 <= x <= gx + gw/2 and
        gy - gh/2 <= y <= gy + gh/2
    )

# ---------------------- COMMANDS ----------------------
class ToggleAllLiveable(Command):
    def __init__(self, position, liveable, *signals):
        self.position = position
        self.liveable = liveable
        if signals:
            self.connect(signals)
    def do(self, *args, pos=None, **kwargs):
        print(f"ToggleLiveable do: {pos}")
        self.liveable.alive = not self.liveable.alive

class ToggleClickedLiveable(Command):
    def __init__(self, position, liveable, *signals):
        self.position = position
        self.liveable = liveable
        if signals:
            self.connect(signals)
    def do(self, *args, pos=None, **kwargs):
        print(f"ToggleLiveable do: {pos}")
        
        if within_grid(pos, self.position):
            self.liveable.alive = not self.liveable.alive



# ---------------------- COMPONENTS ----------------------
class Collider(Component):
    def __init__(self, width=50, height=50, is_solid=True, tag="default"):
        self.width = width
        self.height = height
        self.is_solid = is_solid  # If True, prevents movement through this collider
        self.tag = tag            # For collision filtering

class ParticleEmitter(Component):
    def __init__(self, color=(255, 200, 0), size=5, rate=10, lifetime=0.5, 
                 velocity_range=(-50, 50), max_particles=100):
        self.color = color
        self.size = size
        self.rate = rate          # Particles per second
        self.lifetime = lifetime  # Seconds each particle lives
        self.velocity_range = velocity_range
        self.max_particles = max_particles
        self.time_since_last = 0
        self.particles = []       # List of active particles

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0

class Shine(Component):
    def __init__(self, radius=100, intensity=0.7, color=(255, 255, 255), pulse_speed=1.0):
        self.radius = radius          # How far the shine extends
        self.intensity = intensity    # Base intensity of the shine (0.0-1.0)
        self.color = color            # Color of the shine
        self.pulse_speed = pulse_speed  # Speed of pulsing effect
        self.time = 0                 # Internal timer for pulsing


class Liveable(Component):
    def __init__(self, alive=True):
        self.alive = alive


# ---------------------- SYSTEMS ----------------------
import pygame
import random


class CollisionSystem(System):
    @staticmethod
    def iterate(game, delta_time):
        # Get all entities with both Position and Collider components
        collidables = [e for e in game.entities 
                     if e.has_component(Position) and e.has_component(Collider)]
        
        # get all pairs of collidables
        pairs = list(itertools.combinations(collidables, 2))
        for entity1, entity2 in pairs:
            pos1, col1 = entity1.get_components(Position, Collider)
            pos2, col2 = entity2.get_components(Position, Collider)
            if not (pos1 and pos2 and col1 and col2 and col1.is_solid and col2.is_solid): 
                continue
            
            # Simple AABB collision detection
            if (abs(pos1.x - pos2.x) < (col1.width + col2.width) / 2 and
                abs(pos1.y - pos2.y) < (col1.height + col2.height) / 2):
                # Move entities apart
                vel1 = entity1.get_component(Velocity)
                vel2 = entity2.get_component(Velocity)
                if vel1: vel1.unmove_by_unit_delta(pos1, delta_time)
                if vel2: vel2.unmove_by_unit_delta(pos2, delta_time)

class ParticleSystem(System):
    @staticmethod
    def iterate(game, delta_time):
        for entity in game.entities:
            pos, emitter = entity.get_components(Position, ParticleEmitter)
            vel = entity.get_component(Velocity)
            
            if pos and emitter:
                # Update existing particles
                for particle in emitter.particles[:]:
                    particle.age += delta_time
                    if particle.age >= particle.lifetime:
                        emitter.particles.remove(particle)
                        continue
                    
                    # Move particle
                    particle.x += particle.vx * delta_time
                    particle.y += particle.vy * delta_time
                
                # Emit new particles
                emitter.time_since_last += delta_time
                particles_to_emit = int(emitter.rate * emitter.time_since_last)
                
                if particles_to_emit > 0 and len(emitter.particles) < emitter.max_particles:
                    emitter.time_since_last = 0
                    
                    for _ in range(min(particles_to_emit, emitter.max_particles - len(emitter.particles))):
                        # Create particle with random velocity
                        vx = random.uniform(*emitter.velocity_range)
                        vy = random.uniform(*emitter.velocity_range)
                        
                        # If entity is moving, add its velocity to particles
                        if vel:
                            vx -= vel.vx * vel.unit_pixels_per_second * 0.1  # Trail effect
                            vy -= vel.vy * vel.unit_pixels_per_second * 0.1
                        
                        # Randomize color slightly
                        r, g, b = emitter.color
                        color_variation = 30
                        color = (
                            max(0, min(255, r + random.randint(-color_variation, color_variation))),
                            max(0, min(255, g + random.randint(-color_variation, color_variation))),
                            max(0, min(255, b + random.randint(-color_variation, color_variation)))
                        )
                        
                        particle = Particle(
                            pos.x, pos.y, vx, vy, color, 
                            emitter.size, emitter.lifetime
                        )
                        emitter.particles.append(particle)


def get_screen(game): return next((system.screen for system in game.systems if isinstance(system, PyGameRenderSystem)), None)

class ParticleRenderSystem(System):
    @staticmethod
    def iterate(game, delta_time):
        if not (screen := get_screen(game)): 
            return
            
        for entity in game.entities:
            emitter = entity.get_component(ParticleEmitter)
            if emitter:
                for particle in emitter.particles:
                    # Fade out based on age
                    alpha = 255 * (1 - particle.age / particle.lifetime)
                    size = particle.size * (1 - 0.5 * particle.age / particle.lifetime)
                    
                    # Draw particle
                    pygame.draw.circle(
                        screen,
                        particle.color + (int(alpha),) if len(particle.color) == 3 else particle.color,
                        (int(particle.x), int(particle.y)),
                        max(1, int(size))
                    )

class PygameRenderAliveSystem(System):
    def __init__(self, alive_color=(255, 255, 255), dead_color=(0, 0, 0)):
        self.alive_color = alive_color
        self.dead_color = dead_color
    def iterate(self, game, delta_time):
        for entity in game.entities:
            if entity.has_component(Liveable):
                liveable = entity.get_component(Liveable)
                entity.get_component(Renderable).color = self.alive_color if liveable.alive else self.dead_color


class ChangeGameOfLifeSpeedCommand(Command):
    def do(self, *args, frames_per_change=30, **kwargs): self.obj.frames_per_change = frames_per_change

CHANGE_GAME_OF_LIFE_SPEED = DebugSignal()

class GameOfLifeSystem(System):
    def __init__(self, frames_per_change=30):
        self.frames_per_change = frames_per_change
        self.counter = 0
        self.commands = {ChangeGameOfLifeSpeedCommand(self, CHANGE_GAME_OF_LIFE_SPEED)}
    def iterate(self, game, delta_time):
        self.counter += 1
        if self.counter % self.frames_per_change != 0 or self.frames_per_change <= 0: # change every 120 frames (~2 seconds)
            return
        for entity in [e for e in game.entities if e.has_component(Liveable)]:
            _, i, j = entity.id.split('_')
            i, j = int(i), int(j)
            neighbors = [
                game.get_entity(f'cell_{i+1}_{j}'),
                game.get_entity(f'cell_{i-1}_{j}'),
                game.get_entity(f'cell_{i}_{j+1}'),
                game.get_entity(f'cell_{i}_{j-1}'),
            ]
            # filter None neighbors
            neighbors = [n for n in neighbors if n]
            n_alive_neighbors = sum(n.get_component(Liveable).alive for n in neighbors)
            liveable = entity.get_component(Liveable)
            if liveable.alive:
                liveable.alive = n_alive_neighbors in [2, 3]
            else:
                liveable.alive = n_alive_neighbors == 3





