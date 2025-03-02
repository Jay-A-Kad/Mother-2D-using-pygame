import pygame
import sys
import json
import subprocess
import conclusion
import cv2

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIALOGUE_BOX_COLOR = BLACK  
TEXT_COLOR = (255, 0, 0)  

font_path = "assets/Fonts/Endless Scarry.ttf"
try:
    dialogue_font = pygame.font.Font(font_path, 36)
except:
    dialogue_font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mother Is That You?")
clock = pygame.time.Clock()

bg_image = pygame.image.load('assets/artwork/mother -1.jpg').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

pygame.mixer.init()
pygame.mixer.music.load('assets/Music/final-music.mp3')
pygame.mixer.music.play(-1)

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_spritesheet = pygame.image.load('assets/characters/hero/idle.png').convert_alpha()
        self.run_spritesheet = pygame.image.load('assets/characters/hero/run.png').convert_alpha()

        self.idle_frames = [self.idle_spritesheet.subsurface(pygame.Rect(x, y, w, h)) for x, y, w, h in idleSprites]
        self.run_frames = [self.run_spritesheet.subsurface(pygame.Rect(x, y, w, h)) for x, y, w, h in runSprites]

        self.current_frame_index = 0
        self.animation_speed = 0.1  
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 6, HEIGHT // 1.2)

        self.is_running = False
        self.is_facing_left = False
        self.time_since_last_frame = 0

    def update_animation(self, dt):
        """Update the animation frame based on the current state."""
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.run_frames if self.is_running else self.idle_frames)
            self.image = (self.run_frames if self.is_running else self.idle_frames)[self.current_frame_index]
            
    
            if self.is_facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

    def move(self):
        """Handle player movement and update the running state."""
        keys = pygame.key.get_pressed()
        self.is_running = False
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
            self.is_running = True
            self.is_facing_left = True
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5
            self.is_running = True
            self.is_facing_left = False

    def draw(self, screen):
        """Draw the player on the screen."""
        screen.blit(self.image, self.rect)

    def update(self, dt):
        """Update the player state."""
        self.move()
        self.update_animation(dt)


def handle_dialogue(dialogue_lines, current_line):
    """Display dialogue with text wrapping inside the dialogue box."""
    screen.blit(bg_image, (0, 0))
    pygame.draw.rect(screen, DIALOGUE_BOX_COLOR, (50, HEIGHT - 200, WIDTH - 100, 150))  # Dialogue box

    
    wrapped_lines = wrap_text(dialogue_lines[current_line], dialogue_font, WIDTH - 120)  
    y_offset = HEIGHT - 190  

    for line in wrapped_lines:
        dialogue_text = dialogue_font.render(line, True, TEXT_COLOR)
        screen.blit(dialogue_text, (60, y_offset))
        y_offset += 40  

    pygame.display.flip()


def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '

    if current_line:
        lines.append(current_line.strip())

    return lines



def play_video(video_path):
    """Play a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        cv2.imshow('Video', frame)

        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def save_choice_and_run_conclusion(choice):
    """Save the user's choice and run conclusion.py."""
    choice_data = {"choice": choice}
  
    with open("choice.json", "w") as file:
        json.dump(choice_data, file)
    
   
    subprocess.run(['python3', 'conclusion.py'])
    sys.exit()  



def main():
    player = Player()
    running = True
    dialogue_triggered = False
    video_played = False
    current_line = 0
    dialogue_active = False
    dialogue_lines = [
        "Mother: \"Oh child, you have finally come.                              (Press Enter to Advance)\"",
        "Mother: \"I was waiting for you for almost an eternity.\"",
        "Vile Human: \"Mother? Wh-What are you?\"",
        "Mother: \"Can't you see my child, I am your mother.\"",
        "Vile Human: \"No, it can't be. You are not my mother, you are something else, something evil!\"",
        "Mother: \"I know you have questions. I can answer them.\"",
        "Mother: \"This realm has secrets, and you are one of them.\"",
        "Vile Human: \"Secrets? What are you talking about?\"",
        "Mother: \"Billions of years ago, there were many of us, back then I was known as Xushin\"",
        "Mother: \"I had the ability to divide cells of any living creature , I can change the anatomy of any living being.\"",
        "Mother: \"But, the beings of my kind did not have a liking to my ability , they thought I was an abnormality to their kind\"",
        "Mother: \"So they decided to banish me, they used all their energy to create a planet called earth and they build this underworld...\"",
        "Mother: \"Many years passed, I waited, eventually life began to bloom on earth, there was foilage for the first time in millions of years\"",
        "Mother: \"Using my powers, I accelerated the living growth of this earth\"",
        "Mother: \"I waited until the monkeykind evolved into Humankind\"",
        "Mother: \"The life on earth was not able to make concious descisions, so I waited until...\"",
        "Vile Human: \"Why did you wait for so long?\"",
        "Mother: \"I was waiting fo you my child, Before the beings banished me I had taken the source key the DNA of the Elder being who had made this prison\"",
        "Mother: \"And his blood is the key to unlocking this prison\"",
        "Vile Human: \"So, what has that got to do with me???\"",
        "Mother: \"Using the DNA of the Elders, I created many iterations of you, every single one of them failed\"",
        "Vile Human: \"Wh--What, many versions of me?\"",
        "Mother: \"Yes child, some were born deformed while others lack the will to seek me\"",
        "Mother: \"But, you child , after millenia of failure, you are one true heir of the Elder\"",
        "Mother: \"Now, open the gates for me child, for I shall claim this world\"",
        "Vile Human: \"What will happen to all the surface life, the Humans, the animals, the nature???\"",
        "Mother: \"Ohh, my sweet child! Humans don't mean anything to me, they are mere ants, if they happen to be in my way, I can just step on them and move forward...\"",
        "Mother: \"Now, the time has come my child, sacrifice yourself, so that your mother can rule once again!\"",
        "(1)-You shall rule Mother(Sacrifice Yourself). \n (2)-I shall end my life(Mother Stays in Prison)  \n (3)-I Will not let this happen(You are stuck with Mother for Eternity)",
       
    ]
    branching_dialogues = {
        '1': [
            "Mother: \"Yes, Sweet Child, I always believed in you, my true Heir!\"",
            "Vile Human: \"Blesseth Be Mother!\"",
            "Vile Human: \"The world shall know your chaos once again!\"",
        ],
        '2': [
            "Vile Human: \"I will end myself and stop this madness once and for all.\"",
            "Mother: \"You defy me, vile child of mine, How Dare you defy me?!?!\"",
            "Vile Human: \"I, have the blood of Elders in me, and I know letting you out would be the end of everything\"",
            "Vile Human: \"You shall rot here for eternity, like all the creatures in your Kingdom of Blood!\"",
            "Vile Human: \"I, reject you Mother!\"",
        ],
        '3': [
            "Mother: \"You are evil!\"",
            "Mother: \"I will not let this happen!\"",
            "Mother: \"You defy me, vile child of mine, How Dare you defy me?!?!\"",
            "Vile Human: \"I don't care about you Mother, I reject you!\"",
            "Vile Human: \"This ends with me, I will execute all the versions of me , and will stay here for eternity with you my sweet Mother\"",
            "Vile Human: \"For I have the Elder blood and I am the the one true Heir!\"",
            
        ]
    }
    selected_option = None 

    while running:
        dt = clock.tick(FPS) / 1000.0 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if dialogue_active:
                    if current_line < len(dialogue_lines) - 1:  
                        if event.key == pygame.K_RETURN:
                            current_line += 1
                    elif current_line == len(dialogue_lines) - 1:  # Handle branching
                        if event.key == pygame.K_1:
                            dialogue_lines = branching_dialogues['1']
                            current_line = 0
                            selected_option = '1'
                        elif event.key == pygame.K_2:
                            dialogue_lines = branching_dialogues['2']
                            current_line = 0
                            selected_option = '2'
                        elif event.key == pygame.K_3:
                            dialogue_lines = branching_dialogues['3']
                            current_line = 0
                            selected_option = '3'

        

        if dialogue_active and current_line == len(dialogue_lines) - 1 and selected_option:
            pygame.mixer.music.stop()
            save_choice_and_run_conclusion(selected_option)
            sys.exit()

            running = False
       
        if not dialogue_triggered and player.rect.centerx >= WIDTH // 2:
            dialogue_triggered = True
            dialogue_active = True

        if dialogue_active:
            handle_dialogue(dialogue_lines, current_line)
        else:
            screen.blit(bg_image, (0, 0))  
            player.update(dt)  
            player.draw(screen)
            pygame.display.flip()

        clock.tick(FPS)
        if video_played:
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
