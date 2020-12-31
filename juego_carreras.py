
#GOMEZ VELASCO BRIAN JOSEPH
#PROYECTO - ARQUITECTURA DE COMPUTADORAS
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
pygame.display.set_caption("JUEGO DE CARRERAS")
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
crash_img = pygame.image.load("crash.png")
fondo_intro = pygame.image.load("fondo_intro.jpg")
fondo_intro=pygame.transform.scale(fondo_intro, (800, 600))
intro_musica = pygame.mixer.Sound("music_game.mp3")
        
def intro_loop():
	pygame.mixer.Sound.play(intro_musica)
	intro=True
	while intro:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
				sys.exit()
		gamedisplays.blit(fondo_intro,(0,0))
		

		largetext=pygame.font.Font('freesansbold.ttf',115)
		

		TextSurf,TextRect=text_objects("JUEGO DE",largetext)
		TextRect.center=(400,100)
		gamedisplays.blit(TextSurf,TextRect)


		TextSurf,TextRect=text_objects("CARRERAS",largetext)
		TextRect.center=(400,200)
		gamedisplays.blit(TextSurf,TextRect)

		largetext=pygame.font.Font('freesansbold.ttf',30)
		label = largetext.render("PROYECTO AC - 2020", 1, (249, 53, 14))
		TextRect = label.get_rect()
		TextRect.center=(400,400)
		gamedisplays.blit(label,TextRect)

		label = largetext.render("GOMEZ VELASCO BRIAN JOSEPH", 1, (249, 53, 14))
		TextRect = label.get_rect()
		TextRect.center=(400,450)
		gamedisplays.blit(label,TextRect)



		button("JUGAR",150,520,100,50,green,bright_green,"jugar")
		button("SALIR",550,520,100,50,red,bright_red,"salir")
		pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse=pygame.mouse.get_pos()
	click=pygame.mouse.get_pressed()
	if x+w>mouse[0]>x and y+h>mouse[1]>y:
		pygame.draw.rect(gamedisplays,ac,(x,y,w,h))
		if click[0]==1 and action!=None:        	
			if action=="jugar":
				pygame.mixer.Sound.stop(intro_musica)
				juego_loop()                
			elif action=="salir":
				pygame.mixer.Sound.stop(intro_musica)
				pygame.quit()
				quit()
				sys.exit()
	else:
		pygame.draw.rect(gamedisplays,ic,(x,y,w,h))
	smalltext=pygame.font.Font("freesansbold.ttf",20)
	textsurf,textrect=text_objects(msg,smalltext)
	textrect.center=((x+(w/2)),(y+(h/2)))
	gamedisplays.blit(textsurf,textrect)



def dibujarCoordenadas(frame):
	global coorX, coorY 
	verdeBajo = np.array([36, 100, 20])
	verdeAlto = np.array([70, 255, 255])
	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
	contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for contor in contornos:
		area = cv2.contourArea(contor)
		if area > 600:
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
			cv2.circle(frame,(318,250),170,(255, 255, 0),2)
			cv2.line(frame, (x_medio_der, 0), (x_medio_der, i), (255, 255, 0), 2)
			cv2.line(frame, (x_medio_izq, 0), (x_medio_izq, i), (255, 255, 0), 2)
			dibujarCoordenadas(frame)
			if (coorX > 0 and coorX < x_medio_izq):
				pos_X = -2.5
			if (coorX >= x_medio_izq and coorX <= x_medio_der):
				pos_X = 0
			if (coorX > x_medio_der and coorX < j):
				pos_X = 2.5
			cv2.imshow('camara', frame)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				break
	cap.release()
	cv2.destroyAllWindows()


def text_objects(text,font):
    textsurface=font.render(text,True, blue)
    return textsurface,textsurface.get_rect()

def mensaje_display(text):
    largetext=pygame.font.Font("freesansbold.ttf",80)
    textsurf,textrect=text_objects(text,largetext)
    textrect.center=((display_width/2),(display_height/2))
    gamedisplays.blit(textsurf,textrect)
    pygame.display.update()
    time.sleep(3)
    intro_loop()

def choque(x , y):
	pygame.mixer.music.stop()
	gamedisplays.blit(crash_img, (x,y))
	mensaje_display("CHOQUE!!!")


def car(x,y):
	gamedisplays.blit(carimg,(x,y))

def obstacle(obs_startx,obs_starty,obs):
    if obs==0:
        obs_pic=pygame.image.load("car.jpg")
    elif obs==1:
        obs_pic=pygame.image.load("car1.jpg")
    elif obs==2:
        obs_pic=pygame.image.load("car2.jpg")
    elif obs==3:
        obs_pic=pygame.image.load("car4.jpg")
    elif obs==4:
        obs_pic=pygame.image.load("car5.jpg")
    elif obs==5:
        obs_pic=pygame.image.load("car6.jpg")
    elif obs==6:
        obs_pic=pygame.image.load("car7.jpg")
    gamedisplays.blit(obs_pic,(obs_startx,obs_starty))

def score_system(passed,score,nivel):
    font=pygame.font.SysFont(None,25)
    text=font.render("OBSTACULOS : "+str(passed),True,blue)
    score=font.render("PUNTOS : "+str(score),True,bright_blue)
    nivel_text=font.render("NIVEL : "+str(nivel),True,bright_blue)

    text_rect = text.get_rect(center=(display_width//1.35,50))
    score_rect = score.get_rect(center=(display_width//1.35,30))
    nivel_rect = nivel_text.get_rect(center=(display_width/4,30))

    gamedisplays.blit(text,text_rect)
    gamedisplays.blit(score,score_rect)
    gamedisplays.blit(nivel_text,nivel_rect)

def juego_loop():
	global pos_X
	pygame.mixer.music.load("music2_game.mp3")#Musica de fondo
	pygame.mixer.music.play(-1)#Musica de fondo
	x = 400
	y = 460
	y_change=0
	y2=7
	obs_startx=random.randrange(200,(display_width-200))
	obs_starty=-750
	obs_width=56
	obs_height=125
	passed=0
	level=0
	score=0
	fps=120
	obstacle_speed=5
	obs=0
	bumped=False
	nivel = 1
	while not bumped:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:		
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					pos_X=-2
				if event.key==pygame.K_RIGHT:
					pos_X =2
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
		y2+=obstacle_speed	
		obs_starty-=(obstacle_speed/4)
		obstacle(obs_startx,obs_starty,obs)
		obs_starty+=obstacle_speed
		car(x,y)
		score_system(passed,score,nivel)

		if x>690-car_width or x<110:
			choque(x-15,y-15)
		if x>display_width-(car_width+110) or x<110:
			choque(x-15,y-15)
		if obs_starty>display_height:
			obs_starty=0-obs_height
			obs_startx=random.randrange(170,(display_width-170))
			obs=random.randrange(0,7)
			passed=passed+1
			score=passed*10
			if passed != 0 and passed%20 == 0:
				nivel = nivel+1
				obstacle_speed=obstacle_speed+0.5
		if y<obs_starty+obs_height:
			if x > obs_startx and x < obs_startx + obs_width or x+car_width > obs_startx and x+car_width < obs_startx+obs_width:
				choque(x-15,y-15)
		pygame.display.update()


threadCamera = threading.Thread(target=abrirCamara)
threadCamera.start()
