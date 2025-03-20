'''
https://gameprogrammingpatterns.com/type-object.html
'''
# Breed class: Represents a "type" of monster with shared attributes
class Breed:
    def __init__(self, starting_health, attack_string, parent=None):
        # Store attributes; parent enables inheritance-like behavior
        self.parent = parent
        self.starting_health = starting_health
        self.attack_string = attack_string

    def get_health(self):
        # If health is 0 and there's a parent, inherit from it (dynamic delegation)
        if self.starting_health == 0 and self.parent:
            return self.parent.get_health()
        return self.starting_health

    def get_attack(self):
        # If attack_string is None and there's a parent, inherit (dynamic delegation)
        if self.attack_string is None and self.parent:
            return self.parent.get_attack()
        return self.attack_string

    # Factory method to create a Monster instance of this breed
    def new_monster(self):
        return Monster(self)


# Monster class: The "typed object" that references a Breed
class Monster:
    def __init__(self, breed):
        # Initialize with a breed; health starts at the breed's starting health
        self.breed = breed
        self.health = breed.get_health()

    def get_attack(self):
        # Delegate attack string to the breed
        return self.breed.get_attack()

    def take_damage(self, amount):
        # Simple method to simulate combat
        self.health -= amount
        if self.health <= 0:
            print(f"{self.get_attack()}... but the monster dies!")
        else:
            print(f"{self.get_attack()} (Health left: {self.health})")


# Example usage: Define breeds and create monsters
def main():
    # Base breed: Troll
    troll_breed = Breed(starting_health=25, attack_string="The troll hits you!")

    # Derived breeds inheriting from Troll
    troll_archer_breed = Breed(
        starting_health=0,  # Inherits health from Troll
        attack_string="The troll archer fires an arrow!",
        parent=troll_breed
    )
    troll_wizard_breed = Breed(
        starting_health=0,  # Inherits health from Troll
        attack_string="The troll wizard casts a spell on you!",
        parent=troll_breed
    )

    # Create monsters using the factory method
    troll = troll_breed.new_monster()
    archer = troll_archer_breed.new_monster()
    wizard = troll_wizard_breed.new_monster()

    # Test the monsters
    print("Troll attacks:")
    troll.take_damage(10)  # Health starts at 25, reduces to 15
    print("\nTroll Archer attacks:")
    archer.take_damage(5)  # Health starts at 25 (inherited), reduces to 20
    print("\nTroll Wizard attacks:")
    wizard.take_damage(30)  # Health starts at 25 (inherited), dies

    # Demonstrate flexibility: Add a new breed without changing code
    dragon_breed = Breed(starting_health=230, attack_string="The dragon breathes fire!")
    dragon = dragon_breed.new_monster()
    print("\nDragon attacks:")
    dragon.take_damage(50)  # Health starts at 230, reduces to 180


if __name__ == "__main__":
    main()