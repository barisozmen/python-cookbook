from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from metaclasses import copy_class


# Example usage:
class Original:
    x = 42
    def hello(self):
        return "Hello, world!"

NewClass = copy_class(Original, "NewClass")

# Testing
obj = NewClass()
print(obj.x)           # 42
print(obj.hello())     # "Hello, world!"
print(NewClass.__name__)  # "NewClass"