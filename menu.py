import pygame
import sys
import subprocess
from PIL import Image, ImageSequence

def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")  
        pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        frames.append(pygame.transform.scale(pygame_image, (800, 600)))  
    return frames


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mother The Beginning")
    clock = pygame.time.Clock()

    gif_path = "assets/artwork/menu_background.gif" 
    frames = load_gif_frames(gif_path)
    frame_count = len(frames)
    frame_index = 0

    
    font_path = "assets/fonts/Endless Scarry.ttf"  
    try:
        font = pygame.font.Font(font_path, 40)
    except:
        font = pygame.font.Font(None, 40)  

   
    start_button = pygame.Rect(300, 300, 210, 60)
    exit_button = pygame.Rect(300, 380, 210, 60)

 
    BUTTON_COLOR_IDLE = (30, 30, 30)  
    BUTTON_COLOR_HOVER = (200, 0, 0)  
    BUTTON_TEXT_COLOR = (255, 255, 255)  

    running = True

    while running:
     
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if start_button.collidepoint(mouse_pos):
                        # Start the main game
                        subprocess.run([sys.executable, "main.py"]) 
                        pygame.quit()
                        sys.exit()
                    elif exit_button.collidepoint(mouse_pos):
                       
                        pygame.quit()
                        sys.exit()

      
        screen.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % frame_count

        
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_COLOR_HOVER, start_button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR_IDLE, start_button)

        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_COLOR_HOVER, exit_button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR_IDLE, exit_button)

        
        start_text = font.render("Start Game", True, BUTTON_TEXT_COLOR)
        exit_text = font.render("Exit", True, BUTTON_TEXT_COLOR)
        screen.blit(start_text, (start_button.x + 35, start_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 75, exit_button.y + 10))

        
        pygame.display.flip()
        clock.tick(15) 

if __name__ == "__main__":
    main_menu()
