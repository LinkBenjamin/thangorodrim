import pygame
import sys
from managers.scene_manager import SceneManager

# Global constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60
GAME_TITLE = "Thangorodrim"

def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    scene_manager = SceneManager(screen)
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_events(events)
        
        running = running and scene_manager.update()
        scene_manager.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()