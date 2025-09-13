import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Restart Button Skeleton")

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200, 0, 0)
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

restart_button = Button(100, 150, 200, 60, "RESTART")

running = True
while running:
    screen.fill((0, 0, 0))
    restart_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if restart_button.is_clicked(event):
            print("Restart clicked!")
            # put your reset_game() or lose_screen() call here

    pygame.display.update()

pygame.quit()
