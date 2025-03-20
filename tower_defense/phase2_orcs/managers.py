


from component import *
from command import *




class Manager:
    def __init__(self, game):
        self.game = game
        
    def update(self, delta_time):
        pass
    
    
class OrcManager(Manager):
    def __init__(self, game):
        super().__init__(game)
        ORC_REACHES_GATE.connect(self.on_orc_reaches_gate)
        
    def on_orc_reaches_gate(self, orc):
        print(f"OrcManager Orc {orc} reaches gate")
        self.game.entities.remove(orc)
        del orc
        
    def on_orc_dies(self, orc):
        print(f"Orc {orc} dies")
        self.game.entities.remove(orc)
        del orc
        
        
class GateManager(Manager):
    def __init__(self, game):
        super().__init__(game)
        self.home_points = 1000
        ORC_REACHES_GATE.connect(self.on_orc_reaches_gate)
        
    def on_orc_reaches_gate(self, orc):
        print(f"GateManager Orc {orc} reaches gate")
        self.home_points -= orc.breed.max_health
        print(f"GateManager Home points: {self.home_points}")
        if self.home_points <= 0:
            GAME_OVER.send()
    
class GoldManager(Manager):
    def __init__(self, game):
        super().__init__(game)
        self.gold = 0
        ORC_KILLED.connect(self.on_orc_killed)
        
    def on_orc_killed(self, orc):
        print(f"GoldManager Orc {orc} killed")
        self.gold += orc.breed.max_health
        
        
        
class HoverManager(Manager):
    def __init__(self, game):
        super().__init__(game)
        MOUSE_LEFT_CLICK.connect(self.on_mouse_left_click)
        
    def on_mouse_left_click(self, x, y):
        print(f"HoverManager Mouse left click at {x}, {y}")
        
    def on_mouse_motion(self, x, y):
        print(f"HoverManager Mouse motion at {x}, {y}")
        
        
        