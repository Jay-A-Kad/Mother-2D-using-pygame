
import os
import random
import math
import pygame
from os import listdir
import sys
from os.path import isfile, join
from level0Background import Background
from classNPC import NPC
from skeletorEnemy import SkeletorEnemy
from video_player import play_video 
from portal import Portal
from tile_loader import TileLoader
import level2
from game_over import game_over_screen


pygame.init()
pygame.display.set_caption("Mother The Awakening")

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_VEL = 3
# //////////////////////////////////////////////////////
# Dialogue box parameters
DIALOGUE_BOX = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)
FONT = pygame.font.Font("assets/fonts/Endless Scarry.ttf", 36)
BLOOD_RED = (204, 0, 0)  # Blood red color
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
TYPEWRITER_SPEED = 50
# ///////////////////////////////////////////////////
TILE_SIZE = 16
tile_images = {
    1: 'assets/terrain/underworld.png',  

}


tile_loader = TileLoader(TILE_SIZE, 'assets/level-1._environment.csv')


pygame.mixer.init()


pygame.mixer.music.load('assets/Music/level-0-music.mp3')


pygame.mixer.music.play(-1)  


screen = pygame.display.set_mode((WIDTH, HEIGHT))

idleSprites = [
    (30, 48, 48, 80),
    (158, 48, 48, 80),
    (286, 48, 48, 80),
    (414, 48, 48, 80),
    (542, 48, 48, 80),
]

runSprites = [
    (23, 48, 64, 80),
    (152, 48, 64, 80),
    (280, 48, 64, 80),
    (409, 48, 64, 80),
    (537, 48, 64, 80),
    (665, 48, 64, 80),
    (792, 48, 64, 80),
    (920, 48, 64, 80),
]


heroAttack1 = [
    (0,48,64,80),
    (133,48,64,80),
    (294,48,64,80),
    (413,48,80,80),
    (541,48,80,80),
]

heroAttack2 = [
    (0,48, 48,80),
    (128,48,64,80),
    (238,48,96,80),
    (367,48,96,80),
]


skeletonAttack = [ 
    (0,40,112,96),
    (127,40,112,96),
    (255,40,112,96),
    (375,40,112,96),
    (497,40,112,96),
    (622,40,112,96),
    (497,40,112,96),
]

skeletonIdle = [ 
    (0,64, 64,64),
    (126,64,64,64),
    (255,64,64,64),
    (382,64,64,64),
    (510,64,64,64),
    (638,64,64,64),
    (766,64,64,64),
]




skeletonRun = [
    (0,58, 64,80),
    (130,58,64,80),
    (251,58,64,80),
    (377,58,64,80),
    (507,58,64,80),
    (641,58,64,80),
    (766,58,64,80),
]



skeletonDead = [
    (0,48, 48,80),
    (128,48,64,80),
    (238,48,96,80),
    (367,48,96,80),
]






npcIdle1 = [
    (0, 53, 48, 80),
    (128, 53, 48, 80),
    (255, 53, 48, 80),
    (383, 53, 48, 80),
    (511, 53, 48, 80),
    (639, 53, 48, 80),
    (767, 53, 48, 80),
]

heroDead = [
    (0, 53, 48, 80),
    (128, 53, 48, 80),
    (255, 53, 48, 80),
    (383, 53, 48, 80),
    (511, 53, 48, 80),
    (639, 53, 48, 80),
    (767, 53, 48, 80),
]


def show_game_over_screen(screen):
    font = pygame.font.SysFont("Arial", 40)
    
   
    game_over_text = font.render("Game Over", True, (255, 0, 0))  
    message_text = font.render("You could not seek the mother", True, (255, 0, 0))  

  
    play_again_button = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 60, 200, 50)
    exit_button = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 120, 200, 50)

 
    screen.fill((0, 0, 0)) 
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - 50))

    pygame.draw.rect(screen, (255, 0, 0), play_again_button)  
    pygame.draw.rect(screen, (255, 0, 0), exit_button)  
    
    
    play_again_text = font.render("Play Again", True, (255, 255, 255))  
    exit_text = font.render("Exit", True, (255, 255, 255))  

    screen.blit(play_again_text, (WIDTH // 3 + 50, HEIGHT // 2 + 70))
    screen.blit(exit_text, (WIDTH // 3 + 75, HEIGHT // 2 + 130))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    return "play_again"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()



def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprites(sprite_sheet_path, coords, flip_sprites=False):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    sprites = []
    for x, y, width, height in coords:
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(x, y, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        scaled_surface = pygame.transform.scale(surface, (width // 1, height // 1))  
        sprites.append(scaled_surface)
    if flip_sprites:
        return sprites, flip(sprites)
    return sprites

def get_block(size):
    path = join("assets", "terrain","underworld.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA , 32)
    rect = pygame.Rect(16 , 0 ,size,size)
    surface.blit(image , (0,0), rect)
    return pygame.transform.scale2x(surface)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win , offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)



class Player(pygame.sprite.Sprite):
    
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 5
    JUMP_VEL = 8  
    MAX_JUMP_HEIGHT = 50  


    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.mask = None
        self.is_jumping = False
        self.jump_count = 0
        self.attack_count = 0
        self.attack_1 = False
        self.attack_2 = False
        self.attacking = False  
        self.attack_timer = 0   
        self.health = 100
        self.attack_power = 10  
        self.is_dead = False  

        
        self.idle_right, self.idle_left = load_sprites("assets/characters/hero/idle.png", idleSprites, True)
        self.run_right, self.run_left = load_sprites("assets/characters/hero/run.png", runSprites, True)
        self.attack1_right, self.attack1_left = self.load_sprites("assets/characters/hero/attack1.png", heroAttack1, True)
        self.attack2_right, self.attack2_left = self.load_sprites("assets/characters/hero/attack2.png", heroAttack2, True)
        self.hero_dead = self.load_sprites("assets/characters/hero/Dead.png", heroDead, True)  
        self.sprites = self.idle_left  # Default to idle left

    def take_damage(self, damage):
        if not self.is_dead:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.die()

    def die(self):
        self.is_dead = True
        self.attack_power += 5  
        self.sprites = self.hero_dead 
        self.animation_count = 0  

    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        health_ratio = self.health / 100
        health_width = bar_width * health_ratio
        
        pygame.draw.rect(screen, (255, 215, 0), (10, 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 0, 0), (12, 12, bar_width - 4, bar_height - 4))
        pygame.draw.rect(screen, (255, 0, 0), (12, 12, health_width, bar_height - 4))

    def load_sprites(self, sprite_sheet_path, coords, flip_sprites=False):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sprites = []
        for x, y, width, height in coords:
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(x, y, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface)
        if flip_sprites:
            return sprites, self.flip(sprites)
        return sprites
    
    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel  
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel   
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.is_jumping = False  

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_vel = -self.JUMP_VEL  
            self.jump_count = 0

    def perform_attack1(self):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = len(self.attack1_right) * self.ANIMATION_DELAY
            if self.direction == "left":
                self.sprites = self.attack1_left
            else:
                self.sprites = self.attack1_right
            self.attack_1 = True
            self.attack_2 = False

    def perform_attack2(self):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = len(self.attack2_right) * self.ANIMATION_DELAY
            if self.direction == "left":
                self.sprites = self.attack2_left
            else:
                self.sprites = self.attack2_right
            self.attack_1 = False
            self.attack_2 = True

    def update_sprite(self):
        if self.is_dead:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.hero_dead)
            self.sprite = self.hero_dead[sprite_index]
            self.animation_count += 1
        elif self.x_vel != 0 and not (self.attack_1 or self.attack_2):
            self.sprites = self.run_left if self.direction == "left" else self.run_right
        elif not (self.attack_1 or self.attack_2):
            self.sprites = self.idle_left if self.direction == "left" else self.idle_right

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprites)
        self.sprite = self.sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def attack_collision(self, enemy):
        if self.attacking and self.mask.overlap(enemy.mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
            enemy.take_damage(self.attack_power)

    def loop(self, fps, enemy):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.attack_1 = False
                self.attack_2 = False
        else:
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
            self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

        if self.rect.bottom >= HEIGHT - 10:
            self.landed()

        self.attack_collision(enemy)

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x , self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        self.draw_health_bar(screen)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player,objects, player.y_vel)

def draw(window , objects, offset_x):
    for obj in objects:
        obj.draw(window, offset_x)

def draw_dialogue_text(win, text, font, box, color, speed):
    
    text_surface = font.render(text, True, color)
    text_width = text_surface.get_width()
    if text_width < box.width - 20:
        win.blit(text_surface, (box.x + 10, box.y + 10))
    else:
        
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            if font.size(current_line + word)[0] < box.width - 20:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  

       
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            win.blit(line_surface, (box.x + 10, box.y + 10 + i * 40))

class Tree(Object):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.dialogue_shown = False
        self.dialogues = [
            "(press E to advance Dialogues.)",
            "Vile Human - Ugh... What... what happened? Where am I? This... this isn’t real, right?",
            "Vile Human - What kind of tree is that?",
            "Vile Human - It's horrible, it's disgusting, what in the hell ~is this place",
            "Vile Human - Wait, I see someone. Who is that? Let me speak to him.",
            "(I can move now. Let's use arrow keys for movement.)",
            "ohh-no , what in the hell is that create is it a zombie.",
            "(I can attack using W for attack1 and Q for attack2.)",
            "(I can jump as well, press spacebar.)",
            "Now lets kill that brain-eating skeletor"
        ]
        self.dialogue_index = 0
        self.dialogues_finished = False  

    def interact(self, player):
        if self.rect.colliderect(player.rect) and not self.dialogues_finished:
            self.dialogue_shown = True
        else:
            self.dialogue_shown = False

    def next_dialogue(self):
        if self.dialogue_index < len(self.dialogues) - 1:
            self.dialogue_index += 1
        else:
            self.dialogue_shown = False
            self.dialogues_finished = True  
            self.dialogue_index = 0

    def get_current_dialogue(self):
        return self.dialogues[self.dialogue_index] if not self.dialogues_finished else None



def generate_random_enemies(num_enemies, player, all_sprites, sprite_path):
    
    existing_enemies = [sprite for sprite in all_sprites if isinstance(sprite, SkeletorEnemy)]
    
   
    if len(existing_enemies) < 2 and player.rect.x < 500:
      
        for _ in range(num_enemies):
            if len(existing_enemies) < 3:
               
                random_x = random.randint(700, WIDTH - 100)  
                
                
                random_y = HEIGHT - 240  

                
                enemy = SkeletorEnemy(random_x, random_y, 64, 96, sprite_path, player, scale_factor=2.0)
                
                
                all_sprites.add(enemy)
                existing_enemies.append(enemy)  



def show_choice(screen):
   
    font = pygame.font.Font('assets/fonts/Endless Scarry.ttf', 40)
    choice_text = [
        "1. Go to Court of Blood(Find Mother)",
        "2. Stay Here for Eternity, and ROT!!!",
    ]
    box_rect = pygame.Rect(200, 300, 600, 150)
    pygame.draw.rect(screen, (0, 0, 0), box_rect)  
    pygame.draw.rect(screen, (255, 0, 0), box_rect, 3)  

    for i, text in enumerate(choice_text):
        rendered_text = font.render(text, True, (255, 255, 255))  
        screen.blit(rendered_text, (box_rect.x + 20, box_rect.y + 20 + i * 40))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Go to No-World
                    return 1
                elif event.key == pygame.K_2:  # Stay Here for Eternity
                    return 2



def load_idle_frames(sprite_sheet_path, coords):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    frames = []
    for x, y, width, height in coords:
        frame = pygame.Surface((width, height), pygame.SRCALPHA)  
        rect = pygame.Rect(x, y, width, height)
        frame.blit(sprite_sheet, (0, 0), rect)  
        frames.append(frame)
        return frames




def main(screen):
    clock = pygame.time.Clock()
    block_size = 160
    floor = [Block(i * block_size, HEIGHT - block_size + 50, block_size)
             for i in range(-WIDTH//2 // block_size, (WIDTH * 6) // block_size)]
    background = Background()
    player = Player(50, 100, 24, 24)
    tree = Tree(100, HEIGHT - block_size - 320, 400, 450, "assets/characters/npc/demonTree.png")
    portal = Portal(WIDTH // 2 - 48, HEIGHT // 2 - 64, "assets/terrain/portal.png", [
        (0, 1, 96, 128),
        (125, 1, 96, 128),
        (254, 1, 96, 128),
        (382, 1, 96, 128),
        (510, 1, 96, 128),
        (637, 1, 96, 128),
        (765, 1, 96, 128),
        (893, 1, 96, 128),
        ])
    portal_visible = False

    sprite_sheet_path = "assets/characters/npc/NPC1.png"  
    npc_idle_animation = load_idle_frames(sprite_sheet_path, npcIdle1)


    npc = NPC(1000, HEIGHT - 184, 48, 80, "assets/characters/npc/NPC1.png", [
    "(Press E to Advance Dialgoues)",    
    "A soft, unsettling laugh echoes behind him.",
    "Vile Human spins around to see a figure cloaked in dark robes,",
    "their face hidden beneath a veil.]",
    "Cloaked Figure (voice cold with amusement): Welcome to the Kingdom of Blood, wanderer.",
    " You’ve crossed the veil of mortality and stumbled into our domain.",
    "Vile Human (staggering to his feet, his voice shaking): The... Kingdom of Blood? ",
    "No, no, I didn’t stumble anywhere! I— I was... I don’t even remember!",
    "Cloaked Figure (tilting their head): Few do. The passage between life and this realm strips",
    " away more than just memories. But you are here now, and the blood calls to you. It always calls.",
    "Vile Human(panicked, looking at his hands and body, noticing faint scars and strange markings",
    " that weren’t there before): ",
    "What do you mean 'calls'? What are these? What’s happening to me?",
    "Cloaked Figure (chuckling): The scars tell your story; the blood marks your passage. ",
    "Here, life feeds on the remnants of pain, sacrifice, and betrayal. Perhaps you gave too much.",
    " Perhaps you took too much. Does it matter? You belong to the blood now.",
    "Vile Human(stepping back, voice rising): No! I don’t belong to anything or anyone!",
    "I didn’t ask for this! I need to leave— I need to get out of here!",
    "Cloaked Figure (mockingly): Leave? Oh, my dear lost soul, there is no leaving the Kingdom of Blood. ",
    "Not unless it desires to release you. And it never does.",
    "[The whispering grows louder, and the red light of the sky darkens slightly.",
    " Shadows begin to stir and approach.]",
    "Vile Human (looking around wildly): No. No! I won’t stay here! There has to be a way out!",
    "Cloaked Figure (stepping closer, voice dropping to a sinister whisper):",
    " Run if you like, fight if you dare. But the blood is patient. It will claim you eventually, ",
    "as it claims us all.",
    "Vile Human (gritting his teeth, whispering to himself): Not me. Not today. ",
    "I’ll find a way out of this hell... no matter what it takes.",
    "[He stumbles forward into the unknown, the twisted landscape shifting with every step,",
    " as if alive and watching.]"
    
    ], 
    npc_idle_animation
)

    npc.dialogues_finished = False    

    play_video("assets/artwork/scene-0.mp4")

    offset_x = 0
    scroll_area_width = 200

    dialogue_text = ""  
    current_char = 0  
    last_time = pygame.time.get_ticks()  

    
    all_sprites = pygame.sprite.Group()
    enemy = SkeletorEnemy(400, HEIGHT - 240, 64, 96, "assets/characters/enemies/skeletor", player,scale_factor=2.0)
    all_sprites.add(enemy)

     
    generate_random_enemies(5, player, all_sprites, "assets/characters/enemies/skeletor")

    choice_shown = False  
    run = True
    while run:
        dt = clock.tick(FPS) / 1000
        clock.tick(FPS)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if not player.attacking: 
                    if event.key == pygame.K_SPACE:  
                        player.jump()
                elif event.key == pygame.K_LEFT:
                        player.move_left(PLAYER_VEL)
                elif event.key == pygame.K_RIGHT:
                        player.move_right(PLAYER_VEL)
                if event.key == pygame.K_q:  
                    player.perform_attack1()
                elif event.key == pygame.K_w:  
                    player.perform_attack2()
                if event.key == pygame.K_e:
                   
                    if tree.dialogue_shown:
                        tree.next_dialogue()  
                    else:
                        npc.next_dialogue()  

       
        player.loop(FPS,enemy)
        handle_move(player, floor)
        npc.interact(player)
        if npc.dialogues_finished and not choice_shown:
            choice_shown = True
            choice_result = show_choice(screen)
            if choice_result == 1:
                level2.main()  
                return  # Exit current level
            elif choice_result == 2:
                print("Player chose to stay.")  # Stay here for eternity
        tree.interact(player)
        all_sprites.update()  #

      
       
       
        all_enemies_dead = all(
            isinstance(sprite, SkeletorEnemy) and sprite.health <= 0
            for sprite in all_sprites
        )

        for enemy in all_sprites:
            if isinstance(enemy, SkeletorEnemy):
                enemy.update()  
                enemy.draw(screen)  
                enemy.draw_health_bar(screen)  

        if all_enemies_dead and not portal_visible:
            portal_visible = True  

        if portal_visible:
            portal.update(dt)  
        

       
        if player.health == 0 and not player.is_dead:
            player.die()
            result = show_game_over_screen(screen)
            if result == "play_again":
                main(screen)  # Restart the game
                return
            else:
                pygame.quit()
                sys.exit()

      
     
        player.loop(FPS, enemy)
       
        background.draw(screen, offset_x)
        player.draw(screen, offset_x)
        all_sprites.draw(screen)
        enemy.draw_health_bar(screen)  
        npc.draw(screen, offset_x)
        tree.draw(screen, offset_x)
        
        
        draw(screen, floor, offset_x)
        tile_loader.draw(screen)

       
        player.draw_health_bar(screen)

        
        if npc.show_dialogue:
       
            current_time = pygame.time.get_ticks()
            if current_time - last_time > TYPEWRITER_SPEED and current_char < len(npc.get_current_dialogue()):
                last_time = current_time
                current_char += 1
            dialogue_text = npc.get_current_dialogue()[:current_char]

 
            pygame.draw.rect(screen, BLACK, DIALOGUE_BOX)  
            pygame.draw.rect(screen, GREY, DIALOGUE_BOX, 3)  
            draw_dialogue_text(screen, dialogue_text, FONT, DIALOGUE_BOX, BLOOD_RED, TYPEWRITER_SPEED)

        elif tree.dialogue_shown:
            current_time = pygame.time.get_ticks()
            if current_time - last_time > TYPEWRITER_SPEED and current_char < len(tree.get_current_dialogue()):
                last_time = current_time
                current_char += 1
            dialogue_text = tree.get_current_dialogue()[:current_char]

           
            pygame.draw.rect(screen, BLACK, DIALOGUE_BOX)  
            pygame.draw.rect(screen, GREY, DIALOGUE_BOX, 3)  
            draw_dialogue_text(screen, dialogue_text, FONT, DIALOGUE_BOX, BLOOD_RED, TYPEWRITER_SPEED)

        if((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel >0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

  
        pygame.display.flip()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(screen)