import pygame
import sys
import numpy as np
from ffpyplayer.player import MediaPlayer

def play_video(video_path):
  
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("cutscene-Kingdom of Blood")

    
    player = MediaPlayer(video_path)
    clock = pygame.time.Clock()

   
    button_rect = pygame.Rect(700, 550, 80, 40)

   
    while True:
        frame, val = player.get_frame()
        if val == 'eof':  
            break
        elif frame is None: 
            pygame.time.delay(10)
            continue

       
        img, t = frame
        img_array = np.array(img.to_bytearray()[0]) 
        img_array = img_array.reshape((img.get_size()[1], img.get_size()[0], 3))  

        frame_surface = pygame.surfarray.make_surface(img_array.swapaxes(0, 1))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.close_player()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    player.close_player()
                    return

        
        screen.blit(pygame.transform.scale(frame_surface, (800, 600)), (0, 0))

       
        pygame.draw.rect(screen, (200, 0, 0), button_rect)  
        font = pygame.font.Font('assets/fonts/Endless Scarry.ttf', 24)
        text = font.render("Skip", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 15, button_rect.y + 5))

        pygame.display.flip()
        clock.tick(30)  

    player.close_player()
