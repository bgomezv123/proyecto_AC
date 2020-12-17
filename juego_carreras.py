import pygame
import numpy as np
import time 
import random
import cv2
import threading

pygame.init()
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
pos_X=0

backgroundpic=pygame.image.load("123.jpg")
yellow_strip=pygame.image.load("raya.png")
#strip=pygame.image.load("strip.jpg")
car_width=56


def pointCoordenates(frame):
	global coorX, coorY 
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
			coorX = x
			coorY = y 
			cv2.circle(frame, (x, y), 7, (9, 231, 9), -1)
			cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (9, 231, 9), 1, cv2.LINE_AA)
			contorSuavi = cv2.convexHull(contor) 
			cv2.drawContours(frame, [contorSuavi], 0, (255, 0, 0), 3) 


def openCamera():
	global pos_X,coorX,coorY  
	while (True): 
		ret, frame = cap.read() 
		frame = cv2.flip(frame, 1)
		if ret == True: 
			i = frame.shape[0]
			j = frame.shape[1]
			x_medio_der = int((j + 60) / 2)
			x_medio_izq = int((j - 60) / 2)
			coorX = int(j / 2)
			coorY = int(i / 2)
			cv2.line(frame, (x_medio_der, 0), (x_medio_der, i), (255, 255, 0), 2)
			cv2.line(frame, (x_medio_izq, 0), (x_medio_izq, i), (255, 255, 0), 2)
			pointCoordenates(frame)
			if (coorX > 0 and coorX < x_medio_izq):
				pos_X = -0.7
			if (coorX >= x_medio_izq and coorX <= x_medio_der):
				pos_X = 0
			if (coorX > x_medio_der and coorX < j):
				pos_X = 0.7
			cv2.imshow('camara', frame)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				break
	cap.release()
	cv2.destroyAllWindows()


def car(x,y):  
    gamedisplays.blit(carimg,(x,y))

def juego_loop():
	
	global pos_X
	x = 400
	y = 460
	y_change=0
	y2=7

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:		
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					pos_X=-6
				if event.key==pygame.K_RIGHT:
					pos_X = 6
				if event.key==pygame.K_a:
					obstacle_speed+=2
				if event.key==pygame.K_b:
					obstacle_speed-=2
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
					pos_X=0

		x+=pos_X
		gamedisplays.fill(gray)
		

		rel_y=y2%backgroundpic.get_rect().width
		gamedisplays.blit(backgroundpic,(0,rel_y-backgroundpic.get_rect().width))
		gamedisplays.blit(backgroundpic,(700,rel_y-backgroundpic.get_rect().width))

		if rel_y<800:
				gamedisplays.blit(backgroundpic,(0,rel_y))
				gamedisplays.blit(backgroundpic,(700,rel_y))
				gamedisplays.blit(yellow_strip,(400,rel_y))
				gamedisplays.blit(yellow_strip,(400,rel_y+120))
				gamedisplays.blit(yellow_strip,(400,rel_y+240))
				gamedisplays.blit(yellow_strip,(400,rel_y+360))
				gamedisplays.blit(yellow_strip,(400,rel_y+480))
				gamedisplays.blit(yellow_strip,(400,rel_y+600))
				gamedisplays.blit(yellow_strip,(400,rel_y-120))

		y2+=1

		car(x, y)

		pygame.display.update()



threadCamera = threading.Thread(target=openCamera)
threadCamera.start()
