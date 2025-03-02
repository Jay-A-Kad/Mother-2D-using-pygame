import pygame
import sys
import os
import menu

# Initialize Pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 36)

#
def game_over_screen(screen):
    screen.fill(WHITE)
    
   
    game_over_text = FONT.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

 
    try_again_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 70, 300, 50)

    pygame.draw.rect(screen, BLACK, try_again_button)
    pygame.draw.rect(screen, BLACK, exit_button)

    try_again_text = BUTTON_FONT.render("Try Again", True, WHITE)
    exit_text = BUTTON_FONT.render("Exit", True, WHITE)

    screen.blit(try_again_text, (try_again_button.x + (try_again_button.width - try_again_text.get_width()) // 2,
                                 try_again_button.y + (try_again_button.height - try_again_text.get_height()) // 2))
    screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2,
                            exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

    pygame.display.flip()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if try_again_button.collidepoint(mouse_pos):
                    try_again()
                    sys.exit()
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def try_again():
    menu.main_menu()
    
