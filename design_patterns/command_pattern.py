# SuperGrok AI wrote below python code based on https://gameprogrammingpatterns.com/command.html 
# SuperGrok link: https://x.com/i/grok/share/zD7QZnS4XZDhePte9ozZgAlsU

from abc import ABC, abstractmethod

# Receiver: The object that knows how to perform the actual actions
class GameActor:
    def __init__(self):
        self.position = [0, 0]  # x, y position
        self.is_jumping = False

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy
        print(f"Moved to position: {self.position}")

    def undo_move(self, dx, dy):
        self.position[0] -= dx
        self.position[1] -= dy
        print(f"Undid move, back to position: {self.position}")

    def jump(self):
        self.is_jumping = True
        print("Jumped!")

    def undo_jump(self):
        self.is_jumping = False
        print("Undid jump.")

# Abstract Command
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Concrete Command: Move
class MoveCommand(Command):
    def __init__(self, actor, dx, dy):
        self.actor = actor
        self.dx = dx
        self.dy = dy

    def execute(self):
        self.actor.move(self.dx, self.dy)

    def undo(self):
        self.actor.undo_move(self.dx, self.dy)

# Concrete Command: Jump
class JumpCommand(Command):
    def __init__(self, actor):
        self.actor = actor

    def execute(self):
        self.actor.jump()

    def undo(self):
        self.actor.undo_jump()

# Null Command (for buttons that do nothing)
class NoCommand(Command):
    def execute(self):
        print("No action.")

    def undo(self):
        print("No undo needed.")

# Invoker: Handles input and invokes commands
class InputHandler:
    def __init__(self):
        self.commands = {}  # Map inputs to commands
        self.command_history = []  # For undo support

    def set_command(self, button, command):
        self.commands[button] = command

    def handle_input(self, button):
        command = self.commands.get(button, NoCommand())
        command.execute()
        self.command_history.append(command)

    def undo_last(self):
        if self.command_history:
            last_command = self.command_history.pop()
            last_command.undo()
        else:
            print("Nothing to undo.")

# Example usage
if __name__ == "__main__":
    actor = GameActor()
    handler = InputHandler()

    # Configure commands
    handler.set_command("left", MoveCommand(actor, -1, 0))
    handler.set_command("right", MoveCommand(actor, 1, 0))
    handler.set_command("up", JumpCommand(actor))
    handler.set_command("none", NoCommand())  # Explicit null command

    # Simulate inputs
    handler.handle_input("right")  # Move to [1, 0]
    handler.handle_input("up")     # Jump
    handler.handle_input("left")   # Move to [0, 0]
    handler.handle_input("none")   # No action

    # Undo last two actions
    handler.undo_last()  # Undo no action
    handler.undo_last()  # Undo left move
