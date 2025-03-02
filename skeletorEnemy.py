import pygame
import math


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

class SkeletorEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path, player, scale_factor=1.0):
        super().__init__()

        self.scale_factor = scale_factor  
        self.idle, self.idle_flip = self.load_sprites(f"{sprite_path}/idle.png", skeletonIdle, True)
        self.walk, self.walk_flip = self.load_sprites(f"{sprite_path}/walk.png", skeletonRun, True)
        self.attack, self.attack_flip = self.load_sprites(f"{sprite_path}/attack.png", skeletonAttack, True)
        self.dead, self.dead_flip = self.load_sprites(f"{sprite_path}/dead.png", skeletonDead, True)

        self.sprites = self.idle  # Default to idle state
        self.direction = "left"
        self.animation_count = 0
        self.health = 100
        self.attack_range = 100
        self.move_speed = 1
        self.attack_timer = 0
        self.attacking = False
        self.mask = None
        self.is_dead = False
        self.death_frame_count = 0
        
    
        self.image = self.idle[0]  
        self.rect = self.image.get_rect()  
        self.rect.x = x
        self.rect.y = y
        self.player = player  

    def load_sprites(self, sprite_sheet_path, coords, flip=False):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sprites = []
        for x, y, width, height in coords:
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect = pygame.Rect(x, y, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
        
            scaled_surface = pygame.transform.scale(surface, (int(width * self.scale_factor), int(height * self.scale_factor)))
            sprites.append(scaled_surface)
        if flip:
            flipped_sprites = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
            return sprites, flipped_sprites
        return sprites, [] 

    def update_sprite(self):
       
        if self.attacking:
            self.sprites = self.attack_flip if self.direction == "left" else self.attack
        elif self.is_dead:
            self.sprites = self.dead_flip if self.direction == "left" else self.dead
        elif self.is_near_player():
            self.sprites = self.walk_flip if self.direction == "left" else self.walk
        else:
            self.sprites = self.idle_flip if self.direction == "left" else self.idle

        if self.is_dead:
            sprite_index = self.death_frame_count // 5
            if sprite_index < len(self.sprites):
                self.image = self.sprites[sprite_index]
                self.death_frame_count += 1
            else:
                self.image = self.sprites[-1]  
                self.kill()  
        else:
            sprite_index = (self.animation_count // 5) % len(self.sprites)
            self.image = self.sprites[sprite_index]
            self.animation_count += 1

    def is_near_player(self):
        distance = math.sqrt((self.rect.x - self.player.rect.x) ** 2 + (self.rect.y - self.player.rect.y) ** 2)
        return distance < self.attack_range

    def move_towards_player(self):
        if self.player.rect.x > self.rect.x:
            self.rect.x += self.move_speed
            self.direction = "right"
        elif self.player.rect.x < self.rect.x:
            self.rect.x -= self.move_speed
            self.direction = "left"

    def attack_player(self):
        if self.is_near_player():
            self.attacking = True
            self.attack_timer = len(self.attack) * 5
            self.deal_player_damage()

    def deal_player_damage(self):
        damage = self.player.health * 0.002
        self.player.take_damage(damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0 and not self.is_dead:
            self.die()

    def die(self):
        self.is_dead = True
        self.death_frame_count = 0

    def update(self):
        if self.health > 0 and not self.is_dead:
            if self.is_near_player():
                self.attack_player()
                self.move_towards_player()
            else:
                self.sprites = self.idle_flip if self.direction == "left" else self.idle
            self.update_sprite()
        elif self.is_dead:
            self.update_sprite()

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def draw_health_bar(self, window):
        if self.health > 0:  
            health_bar_width = 50
            health_bar_height = 5
            pygame.draw.rect(window, (0, 0, 0), (self.rect.x + 5, self.rect.y - 10, health_bar_width, health_bar_height))
            pygame.draw.rect(window, (255, 0, 0), (self.rect.x + 5, self.rect.y - 10, (self.health / 100) * health_bar_width, health_bar_height))
