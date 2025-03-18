# Flyweight for Tree rendering (shared intrinsic state)
class TreeModel:
    def __init__(self, mesh, bark_texture, leaves_texture):
        # Intrinsic state: Shared across all tree instances
        self.mesh = mesh
        self.bark_texture = bark_texture
        self.leaves_texture = leaves_texture

    def render(self, position, height, thickness, bark_tint, leaf_tint):
        # Simulate rendering with extrinsic state passed in
        print(f"Rendering tree at {position} with height={height}, "
              f"thickness={thickness}, bark_tint={bark_tint}, leaf_tint={leaf_tint}, "
              f"using mesh={self.mesh}, bark={self.bark_texture}, leaves={self.leaves_texture}")


# Flyweight for Terrain tiles (shared intrinsic state)
class Terrain:
    def __init__(self, movement_cost, is_water, texture):
        # Intrinsic state: Shared across all tiles of this type
        self.movement_cost = movement_cost
        self.is_water = is_water
        self.texture = texture

    def get_movement_cost(self):
        return self.movement_cost

    def is_water(self):
        return self.is_water

    def get_texture(self):
        return self.texture


# Flyweight Factory to manage shared instances
class FlyweightFactory:
    def __init__(self):
        # Pool of flyweight objects
        self._flyweights = {}

    def get_tree_model(self, mesh, bark_texture, leaves_texture):
        # Unique key for this combination of intrinsic state
        key = (mesh, bark_texture, leaves_texture)
        if key not in self._flyweights:
            self._flyweights[key] = TreeModel(mesh, bark_texture, leaves_texture)
        return self._flyweights[key]

    def get_terrain(self, movement_cost, is_water, texture):
        # Unique key for terrain type
        key = (movement_cost, is_water, texture)
        if key not in self._flyweights:
            self._flyweights[key] = Terrain(movement_cost, is_water, texture)
        return self._flyweights[key]


# Tree class with extrinsic state
class Tree:
    def __init__(self, model, position, height, thickness, bark_tint, leaf_tint):
        # Reference to shared flyweight (intrinsic state)
        self.model = model
        # Extrinsic state: Unique to this tree instance
        self.position = position
        self.height = height
        self.thickness = thickness
        self.bark_tint = bark_tint
        self.leaf_tint = leaf_tint

    def render(self):
        # Pass extrinsic state to the flyweight for rendering
        self.model.render(self.position, self.height, self.thickness,
                          self.bark_tint, self.leaf_tint)


# World class for terrain tiles
class World:
    def __init__(self, width, height, factory):
        self.width = width
        self.height = height
        self.factory = factory
        # Grid of flyweight references (pointers to shared Terrain objects)
        self.tiles = [[None for _ in range(height)] for _ in range(width)]
        self._initialize_terrain()

    def _initialize_terrain(self):
        # Simplified terrain generation (similar to text example)
        grass = self.factory.get_terrain(1, False, "grass.png")
        hill = self.factory.get_terrain(3, False, "hill.png")
        river = self.factory.get_terrain(2, True, "river.png")

        # Fill with grass, sprinkle hills, add a river
        import random
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(0, 9) == 0:  # 10% chance of hill
                    self.tiles[x][y] = hill
                else:
                    self.tiles[x][y] = grass
        # Add a vertical river
        river_x = random.randint(0, self.width - 1)
        for y in range(self.height):
            self.tiles[x][y] = river

    def get_tile(self, x, y):
        return self.tiles[x][y]


# Example usage
def main():
    # Create factory for flyweights
    factory = FlyweightFactory()

    # Tree example: Multiple trees sharing one TreeModel
    print("=== Tree Rendering Example ===")
    tree_model = factory.get_tree_model("tree_mesh.obj", "bark.png", "leaves.png")
    tree1 = Tree(tree_model, (0, 0), 10.0, 2.0, "brown", "green")
    tree2 = Tree(tree_model, (5, 5), 12.0, 2.5, "dark_brown", "light_green")
    tree1.render()
    tree2.render()
    print(f"Same model? {tree1.model is tree2.model}")  # True (shared flyweight)

    # Terrain example: World with shared terrain types
    print("\n=== Terrain Tiles Example ===")
    world = World(5, 5, factory)  # 5x5 grid
    # Check a few tiles
    tile1 = world.get_tile(0, 0)  # Likely grass
    tile2 = world.get_tile(2, 2)  # Could be grass, hill, or river
    print(f"Tile at (0,0): Movement cost={tile1.get_movement_cost()}, "
          f"Water={tile1.is_water}, Texture={tile1.get_texture()}")
    print(f"Tile at (2,2): Movement cost={tile2.get_movement_cost()}, "
          f"Water={tile2.is_water}, Texture={tile2.get_texture()}")
    # Verify sharing
    same_grass = factory.get_terrain(1, False, "grass.png")
    print(f"Same grass instance? {tile1 is same_grass}")  # True if both are grass


if __name__ == "__main__":
    main()