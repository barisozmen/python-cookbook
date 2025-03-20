from blinker import Signal



# ---------------------- SIGNALS ----------------------
class DebugSignal(Signal):
    def __init__(self, name=None):
        super().__init__(name)
        self.name = name or f"Signal-{id(self)}"
    def send(self, *args, **kwargs):
        print(f"Signal '{self.name}' was sent with args={args}, kwargs={kwargs}")
        return super().send(*args, **kwargs)
    
    
QUIT, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, \
STOP_HORIZONTAL_MOVE, STOP_VERTICAL_MOVE = [DebugSignal() for _ in range(7)]

# Add new mouse signals
MOUSE_LEFT_CLICK, MOUSE_LEFT_RELEASE, MOUSE_MOTION, MOUSE_DRAG = [DebugSignal() for _ in range(4)]

CHANGE_UPDATE_INTERVAL = DebugSignal()


ORC_REACHES_GATE, ORC_KILLED = [DebugSignal() for _ in range(2)]
GAME_OVER = DebugSignal()
GAME_RESTART = DebugSignal()
