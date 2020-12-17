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

cap = cv2.VideoCapture(0)                 
font = cv2.FONT_HERSHEY_SIMPLEX




def pointCoordenates(frame):
    verdeBajo = np.array([36, 100, 20])
    verdeAlto = np.array([70, 255, 255])    
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contor in contornos:
        area = cv2.contourArea(contor) 
        if area > 3000:
            centros = cv2.moments(contor)
            if (centros["m00"] == 0): centros["m00"] = 1
            x = int(centros["m10"] / centros["m00"])
            y = int(centros["m01"] / centros["m00"])
            cv2.circle(frame, (x, y), 7, (9, 231, 9), -1)
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (9, 231, 9), 1, cv2.LINE_AA)
            contorSuavi = cv2.convexHull(contor) 
            cv2.drawContours(frame, [contorSuavi], 0, (255, 0, 0), 3) 

def openCamera():
    while (True): 
        ret, frame = cap.read() 
        frame = cv2.flip(frame, 1)
        if ret == True:        
            pointCoordenates(frame)        
            cv2.imshow('camara', frame) 
            if cv2.waitKey(1) & 0xFF == ord('s'): 
                break
    cap.release() 
    cv2.destroyAllWindows() 





def car(x,y):  
    gamedisplays.blit(carimg,(x,y))

def juego_loop():
	
	x_change = 0
	x = 400
	y = 460

	while True:
		for event in pygame.event.get():
			car(400, 300)
			if event.type == pygame.QUIT:		
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					x_change=- 1
				if event.key==pygame.K_RIGHT:
					x_change = 1
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
					x_change=0

		gamedisplays.fill(gray)

		x+=x_change
		car(x, y)

		pygame.display.update()


openCamera()