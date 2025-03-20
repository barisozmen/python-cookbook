# Translated to Python from C++ example in https://gameprogrammingpatterns.com/state.html

# Simulated constants and external systems
JUMP_VELOCITY = 10
MAX_CHARGE = 5
IMAGE_STAND = "stand.png"
IMAGE_JUMP = "jump.png"
IMAGE_DUCK = "duck.png"
IMAGE_DIVE = "dive.png"

class Heroine:
    def __init__(self):
        # Initial state is standing
        self.state = StandingState()
        self.y_velocity = 0
        self.graphics = IMAGE_STAND

    def handle_input(self, input):
        # Delegate to current state and handle state transition
        new_state = self.state.handle_input(self, input)
        if new_state:
            old_state = self.state
            self.state = new_state
            self.state.enter(self)  # Call entry action for new state

    def update(self):
        # Delegate to current state
        self.state.update(self)

    def set_graphics(self, image):
        self.graphics = image
        print(f"Graphics set to: {image}")

    def super_bomb(self):
        print("Super Bomb activated!")


# Base state class (equivalent to HeroineState in C++)
class State:
    def handle_input(self, heroine, input):
        return None  # Return None to stay in current state

    def update(self, heroine):
        pass  # Default: no update behavior

    def enter(self, heroine):
        pass  # Default: no entry action


# Concrete state: Standing
class StandingState(State):
    def handle_input(self, heroine, input):
        if input == "PRESS_B":
            heroine.y_velocity = JUMP_VELOCITY
            return JumpingState()
        elif input == "PRESS_DOWN":
            return DuckingState()
        return None

    def enter(self, heroine):
        heroine.set_graphics(IMAGE_STAND)


# Concrete state: Jumping
class JumpingState(State):
    def handle_input(self, heroine, input):
        if input == "PRESS_DOWN":
            heroine.y_velocity = 0  # Stop upward movement for dive
            return DivingState()
        return None

    def enter(self, heroine):
        heroine.set_graphics(IMAGE_JUMP)


# Concrete state: Ducking
class DuckingState(State):
    def __init__(self):
        self.charge_time = 0

    def handle_input(self, heroine, input):
        if input == "RELEASE_DOWN":
            return StandingState()
        return None

    def update(self, heroine):
        self.charge_time += 1
        if self.charge_time > MAX_CHARGE:
            heroine.super_bomb()
            # Could transition to another state here if desired

    def enter(self, heroine):
        heroine.set_graphics(IMAGE_DUCK)


# Concrete state: Diving
class DivingState(State):
    def enter(self, heroine):
        heroine.set_graphics(IMAGE_DIVE)


# Demonstration
def main():
    heroine = Heroine()
    print("Initial state: Standing")

    # Simulate input sequence
    inputs = [
        "PRESS_B",      # Jump
        "PRESS_DOWN",   # Dive
        "PRESS_DOWN",   # No effect (in diving state)
        "RELEASE_DOWN", # No effect (in diving state)
        # Assume landing resets to standing (not implemented here)
    ]

    for i, input in enumerate(inputs):
        print(f"\nStep {i + 1}: Input = {input}")
        heroine.handle_input(input)
        heroine.update()

    # Test ducking and charging
    print("\nTesting Ducking and Charge:")
    heroine.state = DuckingState()  # Force into ducking state
    heroine.state.enter(heroine)
    for _ in range(6):  # Update 6 times to exceed MAX_CHARGE
        heroine.update()


if __name__ == "__main__":
    main()