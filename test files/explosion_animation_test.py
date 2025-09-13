import pygame
import random

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(3, 6)
        self.color = (255, 200, 50)
        self.life = 40
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]

    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.life -= 1
        fade = max(self.life * 6, 0)
        r = min(255, fade)
        g = max(0, fade - 150)
        b = 0
        self.color = (r, g, b)

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def explosion_animation(screen, x, y):
    particles = [Particle(x, y) for _ in range(50)]
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for p in particles:
            p.update()
            p.draw(screen)
        pygame.display.update()
        clock.tick(30)
        particles = [p for p in particles if p.life > 0]
        if not particles:
            running = False

def lose_screen():
    pygame.init()
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("You Lose!")

    #the fonts 
    font = pygame.font.Font(None, 74)
    text = font.render("You Lose!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))

    #setup 
    restart_img = pygame.Surface((200, 60))
    restart_img.fill((200, 0, 0))
    small_font = pygame.font.Font(None, 36)
    label = small_font.render("RESTART", True, (255, 255, 255))

    #our restart button 
    restart_img.blit(label, (40, 15))
    restart_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100, restart_img)
    explosion_animation(screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        
        #we can change where the button will send the user 
        if restart_button.draw(screen):
            lose_screen()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    lose_screen()
