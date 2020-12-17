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
background_arboles=pygame.image.load("123.jpg")
raya_amarilla=pygame.image.load("raya.png")
raya_blanca=pygame.image.load("strip.jpg")
car_width=56

def dibujarCoordenadas(frame):
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


def abrirCamara():
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
			dibujarCoordenadas(frame)
			if (coorX > 0 and coorX < x_medio_izq):
				pos_X = -1
			if (coorX >= x_medio_izq and coorX <= x_medio_der):
				pos_X = 0
			if (coorX > x_medio_der and coorX < j):
				pos_X = 1
			cv2.imshow('camara', frame)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				break
	cap.release()
	cv2.destroyAllWindows()


def text_objects(text,font):
    textsurface=font.render(text,True,black)
    return textsurface,textsurface.get_rect()

def mensaje_display(text):
    largetext=pygame.font.Font("freesansbold.ttf",80)
    textsurf,textrect=text_objects(text,largetext)
    textrect.center=((display_width/2),(display_height/2))
    gamedisplays.blit(textsurf,textrect)
    pygame.display.update()
    time.sleep(3)
    juego_loop()

def choque():
	mensaje_display("CHOQUE!!!")


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
					pos_X=-1.5
				if event.key==pygame.K_RIGHT:
					pos_X =1.5
				if event.key==pygame.K_a:
					obstacle_speed+=2
				if event.key==pygame.K_b:
					obstacle_speed-=2
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
					pos_X=0

		x+=pos_X
		gamedisplays.fill(gray)		
		rel_y=y2%background_arboles.get_rect().width
		gamedisplays.blit(background_arboles,(0,rel_y-background_arboles.get_rect().width))
		gamedisplays.blit(background_arboles,(700,rel_y-background_arboles.get_rect().width))

		if rel_y<800:
			gamedisplays.blit(background_arboles,(0,rel_y))
			gamedisplays.blit(background_arboles,(700,rel_y))
			gamedisplays.blit(raya_amarilla,(400,rel_y))
			gamedisplays.blit(raya_amarilla,(400,rel_y+120))
			gamedisplays.blit(raya_amarilla,(400,rel_y+240))
			gamedisplays.blit(raya_amarilla,(400,rel_y+360))
			gamedisplays.blit(raya_amarilla,(400,rel_y+480))
			gamedisplays.blit(raya_amarilla,(400,rel_y+600))
			gamedisplays.blit(raya_amarilla,(400,rel_y-120))
			gamedisplays.blit(raya_blanca,(120,rel_y-200))
			gamedisplays.blit(raya_blanca,(120,rel_y+20))
			gamedisplays.blit(raya_blanca,(120,rel_y+30))
			gamedisplays.blit(raya_blanca,(680,rel_y-100))
			gamedisplays.blit(raya_blanca,(680,rel_y+20))
			gamedisplays.blit(raya_blanca,(680,rel_y+30))
		y2+=2
		car(x, y)
		if x>690-car_width or x<110:
			choque()
		if x>display_width-(car_width+110) or x<110:
			choque()

		pygame.display.update()
threadCamera = threading.Thread(target=abrirCamara)
threadCamera.start()
