import pygame
import os
import sys

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Load fonts
        font_path = os.path.join("assets", "fonts", "aniron.bold.ttf")
        try:
            self.title_font = pygame.font.Font(font_path, 72)
            self.button_font = pygame.font.Font(font_path, 36)
        except:
            print("Error loading Aniron font. Falling back to default.")
            self.title_font = pygame.font.Font(None, 72)
            self.button_font = pygame.font.Font(None, 36)
            raise

        # Create buttons
        self.buttons = [
            {"text": "New Game", "rect": None, "action": self.new_game},
            {"text": "Load Game", "rect": None, "action": self.load_game},
            {"text": "Options", "rect": None, "action": self.options},
            {"text": "Exit", "rect": None, "action": self.exit_game}
        ]

        # Load background image (placeholder until you add the actual image)
        self.background = None
        try:
            bg_path = os.path.join("assets", "images", "title_bg.jpg")
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            print("Background image not found. Using solid color.")
            raise

        self.current_action = None  # Add this line to track the current action

    def draw(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 20, 40))  # Dark blue-ish background as fallback

        # Draw title
        title_text = self.title_font.render("Thangorodrim", True, (255, 215, 0))  # Golden color
        title_rect = title_text.get_rect(centerx=self.screen_width // 2, y=100)
        self.screen.blit(title_text, title_rect)

        # Draw buttons
        button_y = 300
        for button in self.buttons:
            text_surface = self.button_font.render(button["text"], True, (200, 200, 200))
            text_rect = text_surface.get_rect(centerx=self.screen_width // 2, y=button_y)
            button["rect"] = text_rect  # Store the rect for click detection
            
            # Draw button highlight if mouse is over it
            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 100, 100), text_rect.inflate(20, 10), border_radius=5)
                text_surface = self.button_font.render(button["text"], True, (255, 255, 255))
            
            self.screen.blit(text_surface, text_rect)
            button_y += 70

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            for button in self.buttons:
                if button["rect"] and button["rect"].collidepoint(event.pos):
                    self.current_action = button["text"].lower().replace(" ", "_")

    def new_game(self):
        print("Starting new game...")
        # Add your new game logic here

    def load_game(self):
        print("Loading game...")
        # Add your load game logic here

    def options(self):
        print("Opening options...")
        # Add your options menu logic here

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Return and reset the current action
        action = self.current_action
        self.current_action = None
        return action