import pygame
import sys
import random
import math
import subprocess
import finallevel
from game_over import game_over_screen 
from level2Enemy import SkeletorEnemy

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAVITY = 1
JUMP_VEL = 15
INITIAL_PLAYER_HEALTH = 100
ENEMY_HEALTH = 100
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
FALL_THRESHOLD = HEIGHT  
SCROLL_THRESHOLD = 200  


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mother The Guardians of the Court of Blood")
clock = pygame.time.Clock()

pygame.mixer.init()

pygame.mixer.music.load('assets/Music/level-1-music.mp3')

pygame.mixer.music.play(-1)  

sky = pygame.image.load('assets/terrain/level-2-bg.png').convert_alpha()
middleground = pygame.image.load('assets/terrain/middleground.png').convert_alpha()

sky = pygame.transform.scale(sky, (WIDTH, sky.get_height() * (WIDTH / sky.get_width())))
middleground = pygame.transform.scale(middleground, (WIDTH, middleground.get_height() * (WIDTH / middleground.get_width())))

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


knightAttack1 = [
    (0,16,48,80),
    (64,16,64,80),
    (145,16,80,80),
    (245,16,48,80),
    (313,16,96,96),
]

knightAttack2 = [
    (0,16,48,80),
    (102,16,64,80),
    (206,16,96,80),
    (304,16,96,80),
]

knightIdle = [
    (0, 0, 48, 74),  
    (48, 0, 48, 74),
    (96, 0, 48, 74),
    (144, 0, 48, 74),
]

knightRun = [
    (0, 0, 48, 80),  
    (48, 0, 64, 80),
    (112, 0, 64, 80),
    (176, 0, 64, 80),
    (240, 0, 64, 80),
    (304, 0, 64, 80),
    (368, 0, 48, 80),
]

knightDead = [
    (0,16,48,80),
    (71,16,64,64),
    (153,16,64,48),
    (232,16,64,48),
    (309,16,64,48),
    (385,16,64,48),
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


# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load('assets/terrain/block.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.idle_spritesheet = pygame.image.load('assets/characters/hero/idle.png').convert_alpha()
        self.run_spritesheet = pygame.image.load('assets/characters/hero/run.png').convert_alpha()
        self.attack1_spritesheet = pygame.image.load('assets/characters/hero/attack1.png').convert_alpha()
        self.attack2_spritesheet = pygame.image.load('assets/characters/hero/attack2.png').convert_alpha()

        
        self.idle_frames = [self.idle_spritesheet.subsurface(pygame.Rect(x, y, w, h)) for x, y, w, h in idleSprites]
        self.run_frames = [self.run_spritesheet.subsurface(pygame.Rect(x, y, w, h)) for x, y, w, h in runSprites]
        self.attack1_frames = [self.attack1_spritesheet.subsurface(pygame.Rect(x, y, w, h)) for x, y, w, h in heroAttack1]
        self.attack2_frames = [self.attack2_spritesheet.subsurface(pygame.Rect(x, y, w, h)) for x, y, w, h in heroAttack2]

        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.time_since_last_frame = 0

        
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.state = "idle" 
        self.is_facing_left = False
        self.x_vel = 0
        self.y_vel = 0
        self.health = INITIAL_PLAYER_HEALTH
        self.is_jumping = False
        self.on_ground = False

    def set_state(self, state):
       
        if self.state != state:
            self.state = state
            self.current_frame_index = 0
            self.time_since_last_frame = 0

    def move(self, platforms):
        
        self.x_vel = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x_vel = -5
            self.is_facing_left = True
            self.set_state("run")
        elif keys[pygame.K_RIGHT]:
            self.x_vel = 5
            self.is_facing_left = False
            self.set_state("run")
        else:
            if self.state != "attack1" and self.state != "attack2":
                self.set_state("idle")

        self.rect.x += self.x_vel
        self._handle_horizontal_collision(platforms)

        self.y_vel += GRAVITY
        self.rect.y += self.y_vel
        self._handle_vertical_collision(platforms)

    def attack(self, attack_type):
      
        if attack_type == 1:
            self.set_state("attack1")
        elif attack_type == 2:
            self.set_state("attack2")

    def _handle_horizontal_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.x_vel > 0:  
                    self.rect.right = platform.rect.left
                elif self.x_vel < 0:  
                    self.rect.left = platform.rect.right

    def _handle_vertical_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.y_vel > 0:  
                    self.rect.bottom = platform.rect.top
                    self.y_vel = 0
                    self.on_ground = True
                elif self.y_vel < 0:  
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0

    def jump(self):
        """Handle player jumping."""
        if self.on_ground:
            self.y_vel = -JUMP_VEL

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(0, self.health)  
        if self.health == 0:
            self.game_over()

    def attack_enemy(self, enemy):
        if self.state.startswith("attack") and self.rect.colliderect(enemy.rect):
            damage = 20 if self.state == "attack1" else 35  
            enemy.take_damage(damage)

    def check_fall(self):

        if self.rect.y > FALL_THRESHOLD:
            self.health = 0
            self.kill()

    def check_health(self):
 
        if self.health <= 0:
            self.game_over()

    def game_over(self):
  
        game_over_screen(screen)
 
    def update_animation(self, dt):
    
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame_index += 1

            if self.state == "idle":
                frames = self.idle_frames
            elif self.state == "run":
                frames = self.run_frames
            elif self.state == "attack1":
                frames = self.attack1_frames
            elif self.state == "attack2":
                frames = self.attack2_frames
            else:
                frames = self.idle_frames

            if self.current_frame_index >= len(frames):
                if self.state.startswith("attack"):
                    self.set_state("idle")  
                self.current_frame_index = 0

            self.image = frames[self.current_frame_index]

          
            if self.is_facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

    def draw_health_bar(self, screen):
    
        bar_width = 200  
        bar_height = 20  
        x_pos = WIDTH - bar_width - 20  
        y_pos = 20  

        
        pygame.draw.rect(screen, BLACK, (x_pos, y_pos, bar_width, bar_height))

        
        current_health_width = (self.health / INITIAL_PLAYER_HEALTH) * bar_width
        pygame.draw.rect(screen, RED, (x_pos, y_pos, current_health_width, bar_height))

        
        pygame.draw.rect(screen, WHITE, (x_pos, y_pos, bar_width, bar_height), 2)
   

    def update(self, dt, platforms):
       
        self.move(platforms)
        self.update_animation(dt)

    def draw(self, screen):
       
        screen.blit(self.image, self.rect)

 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, scale_factor=1.0):
        super().__init__()

        self.scale_factor = scale_factor

        # Load and slice sprites
        self.idle_frames = self.load_frames(f"{sprite_path}/Idle.png", knightIdle)
        self.run_frames = self.load_frames(f"{sprite_path}/Run.png", knightRun)
        self.attack1_frames = self.load_frames(f"{sprite_path}/Attack 1.png", knightAttack1)
        self.attack2_frames = self.load_frames(f"{sprite_path}/Attack 2.png", knightAttack2)
        self.dead_frames = self.load_frames(f"{sprite_path}/Dead.png", knightDead)

        # State management
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.state = "idle"  # idle, run, attack1, attack2, dead
        self.is_facing_left = False
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.time_since_last_frame = 0

        # Enemy attributes
        self.health = 100
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.attack_range = 80
        self.attack_counter = 0
        self.attack_interval = 60
        self.is_dead = False

    def load_frames(self, path, frame_data):
        """Load and extract frames from a spritesheet."""
        spritesheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = spritesheet.get_size()
        frames = []
        for x, y, w, h in frame_data:
            if x + w > sheet_width or y + h > sheet_height:
                raise ValueError(f"Frame {x, y, w, h} is outside the bounds of the sprite sheet ({sheet_width}, {sheet_height}).")
            frame = spritesheet.subsurface(pygame.Rect(x, y, w, h))
            scaled_frame = pygame.transform.scale(
                frame,
                (int(w * self.scale_factor), int(h * self.scale_factor))
            )
            frames.append(scaled_frame)
        return frames

    def set_state(self, state):
        """Set the enemy's state."""
        if self.state != state:
            self.state = state
            self.current_frame_index = 0
            self.time_since_last_frame = 0

    def update_animation(self, dt):
        """Update the enemy's animation frames."""
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame_index += 1

            # Select frames based on state
            if self.state == "idle":
                frames = self.idle_frames
            elif self.state == "run":
                frames = self.run_frames
            elif self.state == "attack1":
                frames = self.attack1_frames
            elif self.state == "attack2":
                frames = self.attack2_frames
            elif self.state == "dead":
                frames = self.dead_frames
            else:
                frames = self.idle_frames

            if self.current_frame_index >= len(frames):
                if self.state.startswith("attack"):
                    self.set_state("idle")  # Return to idle after attack
                elif self.state == "dead":
                    self.kill()  # Remove enemy if dead
                self.current_frame_index = 0

            self.image = frames[self.current_frame_index]

            # Flip image if facing left
            if self.is_facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

    def follow_player(self, player):
        """Follow the player while updating the state to run."""
        if self.health <= 0 or self.is_dead:
            return
        if self.rect.x < player.rect.x:
            self.x_vel = 2
            self.is_facing_left = False
            self.set_state("run")
        elif self.rect.x > player.rect.x:
            self.x_vel = -2
            self.is_facing_left = True
            self.set_state("run")
        else:
            self.x_vel = 0
            self.set_state("idle")

    def attack_player(self, player):
        """Attack the player if in range."""
        if self.health <= 0 or self.is_dead:
            return
        if abs(self.rect.centerx - player.rect.centerx) <= self.attack_range:
            if self.attack_counter % 2 == 0:
                self.set_state("attack1")
                player.take_damage(10)
            else:
                self.set_state("attack2")
                player.take_damage(20)
            self.attack_counter += 1

    def apply_gravity(self, platforms):
        """Apply gravity and handle vertical collisions."""
        self.y_vel += 1  # Gravity constant
        self.rect.y += self.y_vel
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.y_vel > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.y_vel = 0
                    self.on_ground = True
                elif self.y_vel < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0

    def take_damage(self, amount):
        """Reduce the enemy's health."""
        self.health -= amount
        if self.health <= 0 and not self.is_dead:
            self.die()

    def die(self):
        """Handle enemy death."""
        self.is_dead = True
        self.set_state("dead")

    def update(self, player, platforms):
        """Update enemy logic."""
        if self.health > 0 and not self.is_dead:
            self.follow_player(player)
            self.apply_gravity(platforms)
            self.attack_player(player)
        self.update_animation(1 / FPS)

    def draw(self, screen):
        """Draw the enemy on the screen."""
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        """Draw a health bar above the enemy."""
        if self.health > 0:
            health_bar_width = 50
            health_bar_height = 5
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_width, health_bar_height))
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.rect.x, self.rect.y - 10, (self.health / 100) * health_bar_width, health_bar_height)
            )



class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, scale_factor=1.0):
        super().__init__()

        
        self.idle_frames = self.load_sprites(f"{sprite_path}/NPC1.png", npcIdle1, scale_factor)
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.time_since_last_frame = 0

       
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dialogue_active = False
        self.dialogue_step = 0
        self.dialogues = []
        self.final_choice_active = False  

    def load_sprites(self, sprite_sheet_path, coords, scale_factor):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sprites = []
        for x, y, width, height in coords:
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect = pygame.Rect(x, y, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            scaled_surface = pygame.transform.scale(
                surface, (int(width * scale_factor), int(height * scale_factor))
            )
            sprites.append(scaled_surface)
        return sprites

    def update_animation(self, dt):
       
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame_index]

    def set_dialogues(self):
        
        self.dialogues = [
            ["(Press Spacebar to Advacne Dialogues)"],
            ["Cloaked Figure: Fought well, Vile Human, no one has defeated the Giants of the Kingdom"],
            ["Cloaked Figure: The Court of Blood is a realm of sacrifice and power."],
            ["Cloaked Figure: In this realm, only those who embrace their blood gain strength."],
            ["Cloaked Figure: To gain strength, you must endure pain. Blood demands sacrifice."],
            ["Cloaked Figure: You must give up memories, your identity, or worse."],
            ["Cloaked Figure: There was a human once just like you he had a deformity.."],
            ["Cloaked Figure: He had few lesser limbs than you, But he died seeking Mother"],
            ["Cloaked Figure: I talked with him once he says, it is as if the blood was calling to him"],
            ["Cloaked Figure: I too had a dream of Mother once, But she never spoke to me again."],
            ["Cloaked Figure: Only the chosen may find Mother. Your actions decide our fate."],
            ["Cloaked Figure: At the end lies either ascension or eternal torment."],
            ["Cloaked Figure: You have proven your worth by defeating the giant"],
            ["Cloaked Figure: Go on champion, the Mother awaits you!"],
            ["Press Y to meet Mother", "Press N to stay here until the next champion arrives."]
        ]

    def handle_choice(self, key):
      
        if self.dialogue_step == len(self.dialogues) - 1:  
            if key == pygame.K_y:  # Option 1: Go to Mother 
                pygame.mixer.music.stop()  
                pygame.mixer.music.load('assets/Music/final-music.mp3') 
                pygame.mixer.music.play(-1)  
                finallevel.main()
            elif key == pygame.K_n:  # Option 2: Stay here
                self.dialogues = [["You are stuck here until the next champion arrives."]]
                self.dialogue_step = 0
                self.final_choice_active = False  
        elif key is None:  
            self.dialogue_step += 1

    def show_dialogue(self):
       
        if self.dialogue_step < len(self.dialogues):
            dialogue_text = self.dialogues[self.dialogue_step][0]
            if self.dialogue_step == len(self.dialogues) - 1:  
                choice_text = '\n'.join(self.dialogues[self.dialogue_step][1:])
                return dialogue_text + '\n' + choice_text
            return dialogue_text
        return ""

    def check_player_proximity(self, player):
       
        distance = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        interaction_radius = 100
        if distance <= interaction_radius:
            self.dialogue_active = True
            return True
        else:
            self.dialogue_active = False
            return False

    def update(self, dt):
       
        self.update_animation(dt)



def handle_dialogue(event, player, npc):
    dialogue_font = pygame.font.Font('assets/fonts/Endless Scarry.ttf', 28)  # Adjusted font size
    options_font = pygame.font.Font('assets/fonts/Endless Scarry.ttf', 30)  # Smaller font for choices

    dialogues = npc.dialogues[npc.dialogue_step]

    
    dialogue_box = pygame.Rect(50, 400, 700, 150)
    pygame.draw.rect(screen, BLACK, dialogue_box)
    pygame.draw.rect(screen, WHITE, dialogue_box, 2)

    
    text_y = 420
    if npc.dialogue_step == len(npc.dialogues) - 1:  
        wrapped_lines = wrap_text(dialogues[0], dialogue_font, 680)
        for wrapped_line in wrapped_lines:
            rendered_text = dialogue_font.render(wrapped_line, True, RED)
            screen.blit(rendered_text, (60, text_y))
            text_y += 40

        for choice in dialogues[1:]:  
            rendered_text = options_font.render(choice, True, RED)
            screen.blit(rendered_text, (60, text_y))
            text_y += 40
    else:  
        wrapped_lines = wrap_text(dialogues[0], dialogue_font, 680)
        for wrapped_line in wrapped_lines:
            rendered_text = dialogue_font.render(wrapped_line, True, RED)
            screen.blit(rendered_text, (60, text_y))
            text_y += 40

   
    if event.type == pygame.KEYDOWN:
        if npc.dialogue_step == len(npc.dialogues) - 1:  
            if event.key == pygame.K_y:  # Option 1
                npc.handle_choice(pygame.K_y)
            elif event.key == pygame.K_n:  # Option 2
                npc.handle_choice(pygame.K_n)
        else:  
            if event.key == pygame.K_SPACE:  
                npc.handle_choice(None)



def wrap_text(text, font, max_width):
    
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    if current_line:
        lines.append(current_line)
    return lines

   


def main():
    player = Player(100, HEIGHT - 150, 50, 50)
    enemy = SkeletorEnemy(200, HEIGHT - 200, 64, 96, "assets/characters/enemies/skeletor", player,scale_factor=2.0)
    npc = None  

    platforms = pygame.sprite.Group()
    for i in range(10):  
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = HEIGHT - PLATFORM_HEIGHT 
        platform = Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.add(platform)

    all_sprites = pygame.sprite.Group(player, enemy, *platforms)

    scroll_offset = 0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_q:
                    player.attack(1)
                if event.key == pygame.K_w:
                    player.attack(2)
                if npc and npc.dialogue_active:
                    handle_dialogue(event, player, npc)  

        screen.fill(WHITE)

        
        player.update(dt, platforms)
        player.move(platforms)

       
        player.attack_enemy(enemy)

        scroll_offset = player.rect.x

        # Draw background
        screen.blit(sky, (scroll_offset % sky.get_width(), 0))
        screen.blit(sky, ((scroll_offset % sky.get_width()) - sky.get_width(), 0))
        screen.blit(middleground, (scroll_offset // 3 % middleground.get_width(), 0))
        screen.blit(middleground, ((scroll_offset // 3 % middleground.get_width()) - middleground.get_width(), 0))

        
        for sprite in all_sprites:
            if isinstance(sprite, NPC):
                sprite.update(dt)  
            elif sprite != player:
                sprite.update(player, platforms)  


       
        all_sprites.draw(screen)

        # Draw player health bar
        player.draw_health_bar(screen)
        enemy.draw_health_bar(screen)

       
        if enemy.health <= 0 and npc is None:
            npc = NPC(WIDTH - 400, HEIGHT - 95, "assets/characters/npc", scale_factor=1.0)
            npc.set_dialogues() 
            all_sprites.add(npc)

        if npc:
            npc.check_player_proximity(player)
            if npc.dialogue_active:
                handle_dialogue(event, player, npc)

        
        player.check_fall()
        player.check_health()

      
        enemy.check_fall(HEIGHT)

        pygame.display.flip()

    pygame.quit()
    quit()



if __name__ == "__main__":
    main()
