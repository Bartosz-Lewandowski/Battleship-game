import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920,1080))
    running = True

    while running:
        for event in pygame.event.get():
            image = pygame.image.load("ship1.png")
            screen.blit(image, (100,100))
            pygame.display.flip()
            screen.fill((236,231,231))
            #screen.blit(bgd_image, (0,0)) tu można wstawić sobie siatkę z narysowanymi polami, ale nie będzie można zmienić wtedy rozmiaru
            image.set_alpha(128) # transparentnośc obrazka (może się przydać do obszaru wokół statku)
            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()


