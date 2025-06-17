import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def draw_hug_effect(surface, pos, time):
    x, y = pos
    for i in range(5):
        radius = 50 + (time * 20 + i * 40) % 300
        alpha = max(0, 255 - radius)
        color = (255, 215, 0, alpha)
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (radius, radius), radius)
        surface.blit(s, (x - radius, y - radius))

time = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((240, 230, 250))
    mouse_pos = pygame.mouse.get_pos()

    draw_hug_effect(screen, mouse_pos, time)

    pygame.display.flip()
    clock.tick(60)
    time += 0.01