
import pygame

class NPC:
    def __init__(self, x, y, width, height, image_path, dialogues, idle_animation):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.dialogues = dialogues
        self.current_dialogue_index = 0
        self.show_dialogue = False
        self.dialogues_finished = False
        self.idle_animation = idle_animation  
        self.animation_count = 0  # 

    def interact(self, player):
        if self.rect.colliderect(player.rect):
            self.show_dialogue = True
        else:
            self.show_dialogue = False

    def next_dialogue(self):
        if self.current_dialogue_index < len(self.dialogues) - 1:
            self.current_dialogue_index += 1
        else:
            self.dialogues_finished = True  
            self.show_dialogue = False

    def get_current_dialogue(self):
        if self.current_dialogue_index < len(self.dialogues):
            return self.dialogues[self.current_dialogue_index]
        return ""

    def draw(self, screen, offset_x):
        frame_index = (pygame.time.get_ticks() // 150) % len(self.idle_animation)
        frame = self.idle_animation[frame_index]  # This will now correctly reference a pygame.Surface
        screen.blit(frame, (self.rect.x - offset_x, self.rect.y))

    # Draw dialogue box if needed
        if self.show_dialogue:
            dialogue_box = pygame.Rect(50, 500, 700, 100)
            pygame.draw.rect(screen, (0, 0, 0), dialogue_box)
            pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 3)
            font = pygame.font.Font(None, 40)
            text = self.get_current_dialogue()
            rendered_text = font.render(text, True, (255, 255, 255))
            screen.blit(rendered_text, (dialogue_box.x + 10, dialogue_box.y + 10))

