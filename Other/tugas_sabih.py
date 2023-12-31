import sys
import pygame
from pygame.locals import *

pygame.int()
surface = pygame.display.set_mode((640, 480))

ball = pygame.image.load("pydroball.png")
ballrect = ball.get_rect()
clock = pygame.time.Clock()

width = surface.get.width()
height = surface.get_height()

speed = [0, 9]
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
    clock.tick(60)
    surface.fill((0, 0, 0))
    ballrect = ballrect.move(speed)
if ballrect.left < 0 or ballrect.right > width:
            speed[0] = speed[0]
if ballrect.top < 0 or ballrect.bottom > height:
    surface.blit(ball, ballrect)
    pygame.display.flip()