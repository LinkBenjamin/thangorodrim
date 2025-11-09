from scenes.title_screen import TitleScreen
from enum import Enum

class GameState(Enum):
    TITLE = "title"
    PLAYING = "playing"
    OPTIONS = "options"
    LOADING = "loading"

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_state = GameState.TITLE
        self.scenes = {
            GameState.TITLE: TitleScreen(screen)
            # Add other scenes as they're created
        }

    def handle_events(self, events):
        for event in events:
            if self.current_state == GameState.TITLE:
                self.scenes[self.current_state].handle_event(event)

    def update(self):
        if self.current_state == GameState.TITLE:
            action = self.scenes[self.current_state].update()
            return self.handle_action(action)
        return True

    def handle_action(self, action):
        if not action:
            return True
            
        if action == "new_game":
            self.current_state = GameState.PLAYING
        elif action == "load_game":
            self.current_state = GameState.LOADING
        elif action == "options":
            self.current_state = GameState.OPTIONS
        elif action == "exit":
            return False
        return True

    def draw(self):
        self.scenes[self.current_state].draw()