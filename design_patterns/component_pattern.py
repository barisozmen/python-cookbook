'''
Allow a single entity to span multiple domains without coupling the domains to
each other.

https://gameprogrammingpatterns.com/component.html
'''

from typing import Dict, List, Any


class Component():
    """Base component class that all components will inherit from."""
    
    def __init__(self):
        self.entity = None
    
    def attach(self, entity):
        self.entity = entity
    
    def update(self, delta_time: float): ...


class TransformComponent(Component):
    """Component that handles position, rotation, and scale."""
    
    def __init__(self, x: float = 0, y: float = 0, rotation: float = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.rotation = rotation
    
    def update(self, delta_time: float):
        # No automatic updates for transform
        pass
    
    def move(self, dx: float, dy: float):
        """Move the entity by the given delta."""
        self.x += dx
        self.y += dy
    
    def rotate(self, angle: float):
        """Rotate the entity by the given angle."""
        self.rotation += angle


class RenderComponent(Component):
    """Component that handles rendering."""
    
    def __init__(self, sprite: str):
        super().__init__()
        self.sprite = sprite
        self.visible = True
    
    def update(self, delta_time: float):
        # In a real game, this might update animation frames
        pass
    
    def render(self):
        """Render the entity to the screen."""
        if self.visible and self.entity:
            transform = self.entity.get_component(TransformComponent)
            if transform:
                print(f"Rendering {self.sprite} at position ({transform.x}, {transform.y}) with rotation {transform.rotation}")
            else:
                print(f"Rendering {self.sprite} at default position")


class PhysicsComponent(Component):
    """Component that handles physics and collision."""
    
    def __init__(self, mass: float = 1.0, velocity_x: float = 0, velocity_y: float = 0):
        super().__init__()
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
    
    def update(self, delta_time: float):
        """Update physics simulation."""
        if self.entity:
            transform = self.entity.get_component(TransformComponent)
            if transform:
                transform.x += self.velocity_x * delta_time
                transform.y += self.velocity_y * delta_time
    
    def apply_force(self, force_x: float, force_y: float):
        """Apply a force to the entity."""
        self.velocity_x += force_x / self.mass
        self.velocity_y += force_y / self.mass


class InputComponent(Component):
    """Component that handles player input."""
    
    def __init__(self, move_speed: float = 5.0):
        super().__init__()
        self.move_speed = move_speed
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
    
    def update(self, delta_time: float):
        """Process input and update entity."""
        if self.entity:
            physics = self.entity.get_component(PhysicsComponent)
            if physics:
                # Reset velocity
                physics.velocity_x = 0
                physics.velocity_y = 0
                
                # Apply velocity based on input
                if self.up_pressed:
                    physics.velocity_y = -self.move_speed
                if self.down_pressed:
                    physics.velocity_y = self.move_speed
                if self.left_pressed:
                    physics.velocity_x = -self.move_speed
                if self.right_pressed:
                    physics.velocity_x = self.move_speed


class Entity:
    """A game entity composed of various components."""
    
    def __init__(self, name: str):
        self.name = name
        self.components: Dict[type, Component] = {}
    
    def add_component(self, component: Component):
        """Add a component to this entity."""
        component_type = type(component)
        self.components[component_type] = component
        component.attach(self)
        return component
    
    def get_component(self, component_type: type) -> Component:
        """Get a component by its type."""
        return self.components.get(component_type)
    
    def update(self, delta_time: float):
        """Update all components."""
        for component in self.components.values():
            component.update(delta_time)


class Game:
    """Simple game class to demonstrate the component pattern."""
    
    def __init__(self):
        self.entities: List[Entity] = []
        self.delta_time = 0.016  # ~60 FPS
    
    def add_entity(self, entity: Entity):
        """Add an entity to the game."""
        self.entities.append(entity)
        return entity
    
    def update(self):
        """Update all entities."""
        for entity in self.entities:
            entity.update(self.delta_time)
    
    def render(self):
        """Render all entities."""
        for entity in self.entities:
            render_component = entity.get_component(RenderComponent)
            if render_component:
                render_component.render()


def main():
    # Create a game
    game = Game()
    
    # Create a player entity
    player = Entity("Player")
    player.add_component(TransformComponent(100, 100))
    player.add_component(RenderComponent("player_sprite.png"))
    player.add_component(PhysicsComponent())
    input_component = player.add_component(InputComponent(10.0))
    game.add_entity(player)
    
    # Create an enemy entity
    enemy = Entity("Enemy")
    enemy.add_component(TransformComponent(200, 150))
    enemy.add_component(RenderComponent("enemy_sprite.png"))
    enemy.add_component(PhysicsComponent(2.0, -1.0, 0))
    game.add_entity(enemy)
    
    # Simulate some game loops
    print("Game Start")
    print("-" * 50)
    
    # Simulate player input
    input_component.right_pressed = True
    input_component.down_pressed = True
    
    # Run a few game loops
    for i in range(5):
        print(f"\nFrame {i+1}:")
        game.update()
        game.render()
    
    print("\nChanging player direction")
    input_component.right_pressed = False
    input_component.down_pressed = False
    input_component.left_pressed = True
    input_component.up_pressed = True
    
    # Run a few more game loops
    for i in range(5, 10):
        print(f"\nFrame {i+1}:")
        game.update()
        game.render()
    
    print("-" * 50)
    print("Game End")


if __name__ == "__main__":
    main()
