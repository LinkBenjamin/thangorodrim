import sys
import types

# --- fake dependencies inserted BEFORE importing scene_manager ---
# noop pygame so any imports succeed in tests
sys.modules.setdefault("pygame", types.ModuleType("pygame"))

# define DummyTitleScreen early and expose as scenes.title_screen.TitleScreen
class DummyTitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.handled_events = []
        self.update_action = None
        self.draw_called = False

    def handle_event(self, event):
        self.handled_events.append(event)

    def update(self):
        return self.update_action

    def draw(self):
        self.draw_called = True

mod = types.ModuleType("scenes.title_screen")
mod.TitleScreen = DummyTitleScreen
sys.modules["scenes.title_screen"] = mod
# -----------------------------------------------------------------

from managers import scene_manager as scene_manager_module
from managers.scene_manager import SceneManager, GameState

class DummyScreen:
    pass

def test_initial_state_and_scene_creation():
    screen = DummyScreen()
    manager = SceneManager(screen)

    assert manager.current_state == GameState.TITLE
    assert isinstance(manager.scenes[GameState.TITLE], DummyTitleScreen)
    assert manager.scenes[GameState.TITLE].screen is screen

def test_handle_events_delegates_to_title_screen():
    screen = DummyScreen()
    manager = SceneManager(screen)

    events = ["event1", "event2", 123]
    manager.handle_events(events)

    ts = manager.scenes[GameState.TITLE]
    assert ts.handled_events == events

def test_update_transitions_and_return_values():
    screen = DummyScreen()
    manager = SceneManager(screen)
    ts = manager.scenes[GameState.TITLE]

    ts.update_action = "new_game"
    assert manager.update() is True
    assert manager.current_state == GameState.PLAYING

    manager.current_state = GameState.TITLE
    ts.update_action = "load_game"
    assert manager.update() is True
    assert manager.current_state == GameState.LOADING

    manager.current_state = GameState.TITLE
    ts.update_action = "options"
    assert manager.update() is True
    assert manager.current_state == GameState.OPTIONS

    manager.current_state = GameState.TITLE
    ts.update_action = "exit"
    assert manager.update() is False

    manager.current_state = GameState.TITLE
    ts.update_action = None
    assert manager.update() is True
    assert manager.current_state == GameState.TITLE

def test_draw_delegates_to_scene_draw():
    screen = DummyScreen()
    manager = SceneManager(screen)
    ts = manager.scenes[GameState.TITLE]

    assert not ts.draw_called
    manager.draw()
    assert ts.draw_called is True