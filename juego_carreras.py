import pygame
import numpy as np
import time 
import random
import cv2

pygame.init() #Inicializamos la librería pygame

font = pygame.font.Font('freesansbold.ttf', 32)

gray=(119,118,110)
black=(0,0,0)
red=(255,0,0)
green=(0,200,0)
blue=(0,0,200)
bright_red=(255,0,0)
bright_green=(0,255,0)
bright_blue=(0,0,255)

display_width=800
display_height=600
pygame.display.set_caption("car game")
gamedisplays=pygame.display.set_mode((display_width,display_height))

carimg=pygame.image.load('car1.png')
carimg=pygame.transform.scale(carimg, (56, 125))

def car(x,y):
    
    gamedisplays.blit(carimg,(x,y))

while True:

    gamedisplays.fill(gray)

    car(400, 300)
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    	
    		pygame.quit()
    		quit()
    	pygame.display.update()

