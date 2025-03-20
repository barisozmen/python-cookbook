from base import *
from advanced import *


black = (0, 0, 0)
dark_gray = (100, 100, 100)
light_gray = (200, 200, 200)
dark_green = (0, 20, 0)
light_green = (0, 255, 0)
button_blue = (50, 100, 200)
button_red = (200, 50, 50)




class TextComponent(Component):
    def __init__(self, text, font_size=20, color=light_gray):
        self.text = text
        self.font_size = font_size
        self.color = color




class PygameMonitorSystem(System):
    def __init__(self):
        self.first_time = True
        
    def iterate(self, game, delta_time):
        self.screen = get_screen(game)
        
        liveables = [e.get_component(Liveable) for e in game.entities if e.has_component(Liveable)]
        alive_count = sum(liveable.alive for liveable in liveables)
        dead_count = len(liveables) - alive_count
        
        # Get current game speed (frames per change)
        game_speed = getattr(game, 'frames_per_change', -1)
        speed_text = "Paused" if game_speed < 0 else f"{game_speed} frames"
        
        screen_width, screen_height = self.screen.get_size()
        
        # Prepare text to display
        font = pygame.font.SysFont('Arial', 18)
        
        for text_content, position in [
            (f"Alive: {alive_count}", (20, screen_height - 40)),
            (f"Dead: {dead_count}", (screen_width // 2 - 50, screen_height - 40)),
            (f"Speed: {speed_text}", (screen_width - 150, screen_height - 40))
        ]:
            rendered_text = font.render(text_content, True, 'white')
            self.screen.blit(rendered_text, position)
        


game_of_life = BasicGame(
    *[Entity(
        (pos := Position(x=10+i*20, y=10+j*20, width=16, height=16)),
        (liveable := Liveable(alive=False)),
        Renderable(pos=pos, color=dark_green),
        ToggleClickedLiveable(pos, liveable, MOUSE_LEFT_CLICK, MOUSE_DRAG),
        ToggleAllLiveable(liveable, HALLOWEEN_BUTTON_CLICK),
        id='cell_'+str(i)+'_'+str(j),
    ) for i in range(40) for j in range(40)],
    PyGameInputSystem(),
    GameOfLifeSystem(),
    PygameRenderAliveSystem(alive_color=light_green, dead_color=dark_green),
    PyGameRenderSystem(bg_color=black, screen_size=(900, 900)),
    PygameMonitorSystem(),
    PygameDisplayFlipSystem(),
)



alive_cells = [
    'cell_'+str(random.randint(14, 26))+'_'+str(random.randint(14, 26))
    for _ in range(100)
]

for entity in game_of_life.entities:
    if entity.id in alive_cells:
        entity.get_component(Liveable).alive = True


game_of_life.loop()