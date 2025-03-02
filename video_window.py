import pygame
import sys
import cv2

def play_video_in_window(video_path, window_width, window_height):

    pygame.mixer.quit()  
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error:  video file.")
        return

 
    original_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    scale = min(window_width / original_width, window_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    
    video_screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Video Playback")

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

       
        frame = cv2.resize(frame, (new_width, new_height))

      
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)

      
        x_offset = (window_width - new_width) // 2
        y_offset = (window_height - new_height) // 2
        video_screen.fill((0, 0, 0))  
        video_screen.blit(frame_surface, (x_offset, y_offset))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.release()
                pygame.quit()
                sys.exit()

    video.release()
    pygame.mixer.init()  
