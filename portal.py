import pygame

class Portal:
    def __init__(self, x, y, sprite_sheet_path, animation_frames):
    
        self.x = x
        self.y = y
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 100  
        self.rect = pygame.Rect(x, y, animation_frames[0][2], animation_frames[0][3])

    def update(self, dt):
       
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def draw(self, screen):
      
        frame = self.animation_frames[self.current_frame]
        frame_surface = self.sprite_sheet.subsurface(pygame.Rect(frame))
        screen.blit(frame_surface, (self.x, self.y))
