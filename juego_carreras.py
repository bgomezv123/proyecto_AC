import pygame
import numpy as np
import time 
import random
import cv2

pygame.init() #Inicializamos la librería pygame

font = pygame.font.Font('freesansbold.ttf', 32)

black = (0, 0, 0)
white = (255, 255, 255)
green = (44, 215, 223)
red = (255, 67, 34)
blue = (77, 77, 77)

display_width=800
display_height=600
gamedisplays=pygame.display.set_mode((display_width,display_height))

text = font.render('HOLA', True, green, blue)
textRect = text.get_rect()
textRect.center = (display_width// 2, display_height // 2)

while True:

    gamedisplays.fill(black)
    gamedisplays.blit(text, textRect)

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    	
    		pygame.quit()
    		quit()
    	pygame.display.update()

