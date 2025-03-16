
from base import *
from advanced import *

game = BasicGame(
    World(), 
    Entity().with_components(
        (pos := Position(x=400, y=300)),
        Renderable(color=(0, 100, 255), pos=pos),
        (velocity := Velocity()),
        PlayerControlsVelocity(velocity),
        Collider(width=50, height=50),
        ParticleEmitter(color=(100, 200, 255), size=3, rate=30, lifetime=0.7),
    ),
    # Add a wall to demonstrate collision
    Entity().with_components(
        (pos := Position(x=600, y=300)),
        Renderable(color=(100, 100, 100), pos=pos),
        Collider(width=50, height=200),
    ),
    # Add a wall to demonstrate collision
    Entity().with_components(
        (pos := Position(x=100, y=300)),
        Renderable(color=(50, 60, 100), pos=pos),
        # Collider(width=50, height=50),
    ),
    PyGameInputSystem(),
    MovementSystem(), 
    CollisionSystem(),
    ParticleSystem(),
    PyGameRenderSystem(),
    ParticleRenderSystem(),
)

game.loop()