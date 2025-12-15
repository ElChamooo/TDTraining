import pygame
from collections import deque

class DebugConsole:
    def __init__(self, x, y, w, h, font_size=16):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont("consolas", font_size)
        self.lines = deque(maxlen=200)

    def log(self, text):
        self.lines.append(str(text))

    def draw(self, screen):
        pygame.draw.rect(screen, (20, 20, 20), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        y = self.rect.y + 5
        for line in list(self.lines)[-20:]:
            txt = self.font.render(line, True, (0, 255, 0))
            screen.blit(txt, (self.rect.x + 5, y))
            y += self.font.get_height()
        return screen