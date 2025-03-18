'''
https://gameprogrammingpatterns.com/prototype.html
'''
import copy


class InventoryMixin:
    inventory = []
    def add_to_inventory(self, item):
        self.inventory.append(item)

class AbilitiesMixin:
    abilities = {}
    def add_ability(self, name, power):
        self.abilities[name] = power

class GameCharacter(InventoryMixin, AbilitiesMixin):
    def __init__(self, name="", health=100, attack=10, defense=10):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
    def __str__(self):
        return f"{self.name}: {self.health} health, {self.attack} attack, {self.defense} defense"

class Spawner:
    def __init__(self, prototype):
        self.prototype = prototype
    def spawn(self):
        return copy.deepcopy(self.prototype)

# Example usage
if __name__ == "__main__":
    # Create prototype characters
    warrior = GameCharacter(name="Warrior", health=200, attack=20, defense=15)
    warrior.add_to_inventory("Sword")
    warrior.add_to_inventory("Shield")
    warrior.add_ability("Slash", 25)
    warrior_spawner = Spawner(warrior)
    
    mage = GameCharacter(name="Mage", health=100, attack=30, defense=5)
    mage.add_to_inventory("Staff")
    mage.add_to_inventory("Potion")
    mage.add_ability("Fireball", 40)
    mage_spawner = Spawner(mage)
    
    # Clone characters for players
    player1_character = warrior_spawner.spawn()
    player1_character.name = "Player1's Warrior"
    
    player2_character = mage_spawner.spawn()
    player2_character.name = "Player2's Mage"
    
    # Modify the cloned character without affecting the prototype
    player1_character.health = 180
    player1_character.add_to_inventory("Health Potion")
    
    # Print character information
    print("Prototypes:")
    print(warrior)
    print(f"Inventory: {warrior.inventory}")
    print(f"Abilities: {warrior.abilities}")
    print(mage)
    print(f"Inventory: {mage.inventory}")
    print(f"Abilities: {mage.abilities}")
    
    print("\nCloned Characters:")
    print(player1_character)
    print(f"Inventory: {player1_character.inventory}")
    print(f"Abilities: {player1_character.abilities}")
    print(player2_character)
    print(f"Inventory: {player2_character.inventory}")
    print(f"Abilities: {player2_character.abilities}")