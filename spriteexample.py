import os
import pygame
from constants import *
from BULLETS import Bullet
from mob import Mob
import random

game_folder=os.path.dirname(__file__)
imgfolder=os.path.join(game_folder,"img")
font_folder=os.path.join(game_folder,"fonts")



speed_road=0

#initialze pygame and create window
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HIEGHT))
pygame.display.set_caption("SHOOT EM UP")
clock = pygame.time.Clock()




font_name ='/home/parth/pygame/pokemon.ttf'
sndfolder=os.path.join(game_folder,"sounds")

##LOAD ALL IN GRAPHICS
background=pygame.image.load(os.path.join(imgfolder,"background.png")).convert()

background=pygame.transform.scale(background,(WIDTH,HIEGHT))
background_rect=background.get_rect()
mini_player=pygame.image.load(os.path.join(imgfolder,"car.png")).convert()
mini_player=pygame.transform.scale(mini_player,(25,19))
mini_player.set_colorkey(BLACK)
explosion_anim={}
explosion_anim['player']=[]


explosion_anim['lg']=[]
explosion_anim['sm']=[]

for i in range(9):
	filename ="regularExplosion0{}.png".format(i)
	pname="sonicExplosion0{}.png".format(i)
	expl = pygame.image.load(os.path.join(imgfolder,filename)).convert()
	expl_player=pygame.image.load(os.path.join(imgfolder,pname)).convert()
	expl.set_colorkey(BLACK)
	expl_player.set_colorkey(BLACK)
	img_player=pygame.transform.scale(expl_player,(50,50))
	img_lg=pygame.transform.scale(expl,(75,75))
	explosion_anim['lg'].append(img_lg)
	explosion_anim['player'].append(img_player)

	img_sm=pygame.transform.scale(expl,(30,30))
	explosion_anim['sm'].append(img_sm)

def draw_text(surf,text,size,x,y):
	font =pygame.font.Font(font_name,size)
	text_surface = font.render(text,True,WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop=(x,y)

	surf.blit(text_surface,text_rect)


def draw_shield_bar(surf,x,y,pct,full):

	if pct<0:
		pct=0
	
	fill=(float(pct)/full)*100

	outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
	fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
	#draw_text(surf,str(pct),10,WIDTH-10,HIEGHT-10)
	#if fill<80:
	#	pygame.draw.rect(surf,RED,fill_rect)
	#else:	
	per_red=int(255*(1-(float(pct)/float(full))))
	per_green=int(255*(float(pct)/float(full)))
	pygame.draw.rect(surf,(0,255,0),fill_rect)
	pygame.draw.rect(surf,WHITE,outline_rect,2)






	




class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join(imgfolder,"car.png")).convert()
		self.image.set_colorkey(BLACK)
		self.image=pygame.transform.scale(self.image,(120,200))
		self.radius=20
		#self.image=pygame.Surface((50,40))
		#self.image.fill(GREEN)
		self.rect=self.image.get_rect()
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.rect.center =  (WIDTH/2,HIEGHT/2)
		
		self.rect.bottom=HIEGHT-200
		self.shield=100
		self.speedx=0
		self.lives=3
		self.hidden = False
		self.hide_timer=pygame.time.get_ticks()
		self.shoot_delay=200
		self.last_shot=pygame.time.get_ticks()
		self.speedy=0

	def update(self):
		if self.hidden and pygame.time.get_ticks()-self.hide_timer>1000:
			self.hidden=False
			self.rect.center =  (WIDTH/2,HIEGHT/2)
			self.rect.bottom=HIEGHT-200
		self.speedx=0
		self.speedy=0
		keystate=pygame.key.get_pressed()						
		if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
			self.speedx=-4
			
		if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
			self.speedx=+4
		'''if keystate[pygame.K_UP] or keystate[pygame.K_w]:
			self.speedy=-5
		if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
			self.speedy=+5'''
		if keystate[pygame.K_SPACE]:
			
			self.shoot()
		if self.rect.right>WIDTH:
			self.rect.right=WIDTH
		if self.rect.left<0:
			self.rect.left=0
		if self.rect.top>HIEGHT:
			self.rect.top=HIEGHT
		if self.rect.bottom<0:
			self.rect.bottom=0
		self.rect.x+=self.speedx
		self.rect.y+=self.speedy

		#self.rect.y+=5
		##if self.rect.left>WIDTH:
		##	self.rect.right=0
		#if self.rect.bottom>HIEGHT:
			#self.rect.top=0
	def shoot(self):
		now=pygame.time.get_ticks()
		if now-self.last_shot>self.shoot_delay:
			self.last_shot=now
			bullet=Bullet(self.rect.centerx,self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)
			shoot_sound.play()

	def hide(self):
		self.hidden=True
		self.hide_timer=pygame.time.get_ticks()
		self.rect.center=(WIDTH/2,200+HIEGHT)


	


class strips(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((20,80))
		self.image.fill(WHITE)
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.speedy=0
		self.nitro=500
		self.timer=pygame.time.get_ticks()
		


	def update(self):
		
		
		keystate=pygame.key.get_pressed()						
		

		if self.nitro>20:
			if keystate[pygame.K_UP] or keystate[pygame.K_w]:
				self.accelerate(True)
				if(self.nitro>0):
					self.nitro-=2

		if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
			self.accelerate(False)
			if(self.nitro<500):
				self.nitro+=2

		if keystate[pygame.K_b]:
			self.speedy=0
		if self.nitro<500:	
			self.nitro+=1
		


		global speedo
		speedo=self.speedy

		global nitr
		nitr=self.nitro

		self.accelerate(False)
		self.rect.y+=self.speedy


		if self.rect.top>=HIEGHT:
			self.rect.top=0
		elif self.rect.bottom<=0:

			self.rect.top=HIEGHT

		

	def accelerate(self,check):
		
			if check == True:
				if self.speedy<8:
					self.speedy+=0.1
			else :
				if self.speedy >=0.05:
					self.speedy-=0.05


class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size=size
		self.image=explosion_anim[self.size][0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.last_update=pygame.time.get_ticks()
		self.frame_rate =90


	def update(self):
		now=pygame.time.get_ticks()
		if now-self.last_update>self.frame_rate:
			self.last_update=now
			self.frame+=1
			if self.frame== len(explosion_anim[self.size]):
				self.kill()
			else:
				center=self.rect.center
				self.image =explosion_anim[self.size][self.frame]
				self.rect=self.image.get_rect()
				self.rect.center=center


def draw_lives(surf,x,y,lives,img):
	 for i in range(lives):
	 	img_rect = img.get_rect()
	 	img_rect.x=x+20*i
	 	img_rect.y=y
	 	surf.blit(img,img_rect)


def show_go_screen():
	screen.blit(background,background_rect)
	draw_text(screen,"STREET RACER 1.0!",64,WIDTH/2,HIEGHT/4)
	draw_text(screen,"Arrow keys move,Space to fire",40,WIDTH/2,HIEGHT/2)
	draw_text(screen,"PRESS a key to begin",30,WIDTH/2,HIEGHT-50)
	

	pygame.display.flip()
	waiting=True

	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type==pygame.KEYUP:
				start=True
				waiting=False











##LOAD SOUNDS
shoot_sound=pygame.mixer.Sound(os.path.join(sndfolder,"Laser_Shoot16.wav"))
explode_sound=pygame.mixer.Sound(os.path.join(sndfolder,"Explosion10.wav"))
pygame.mixer.music.load(os.path.join(sndfolder,"badguy.mp3"))
pygame.mixer.music.set_volume(0.5)




pygame.mixer.music.play()

#GAME LOOP
game_over=True 
start=0;
running=True
while running:
	

	if game_over:
		show_go_screen()
		game_over=False
		all_sprites = pygame.sprite.Group()
		player=Player()
		all_sprites.add(player)
		bullets=pygame.sprite.Group()
		mobs=pygame.sprite.Group()

		for i in range(3):
			m= Mob(player.speedy,i)
			mobs.add(m)

		strip=pygame.sprite.Group()


		for i in range(4):
			m=strips(WIDTH/3,((HIEGHT*2*i)/8))	
			
			strip.add(m)

		for i in range(4):
			m=strips((WIDTH*2)/3,((HIEGHT*2*i)/8))	
			
			strip.add(m)

		score=0
	##keep loop running at right speed

	clock.tick(FPS)
	
	#Process input(events)

	for event in pygame.event.get():
		##for exit button
		if event.type==pygame.QUIT:
			running = False
		
	#update
	all_sprites.update()
	strip.update()
	mobs.update(speedo)
	

	#collision b/w mob and bullet
	hits=pygame.sprite.groupcollide(mobs,bullets,True,True)

	for hit in hits:
		

		exp=Explosion(hit.rect.center,'lg')
		all_sprites.add(exp)

		explode_sound.play()
		score+=int(50)

		m=Mob(player.speedy,random.randrange(1,4))
	
		mobs.add(m)

	#COllision b/w mob and player
	hits= pygame.sprite.spritecollide(player,mobs,True,)
	
	for hit in hits:
		m=Mob(player.speedy,random.randrange(1,4))
		
		mobs.add(m)

		player.shield-=40
		 
		exp=Explosion(hit.rect.center,'sm')
		all_sprites.add(exp)
		if player.shield<=0:
			death=Explosion(player.rect.center,'player')
			all_sprites.add(death)
			player.hide()
			player.lives-=1
			player.shield=100

			

	if  player.lives ==0  and not death.alive():
		game_over=True


	#Draw/render		
	screen.fill(BLACK)
	screen.blit(background,background_rect)
	
	strip.draw(screen)
	all_sprites.draw(screen)
	mobs.draw(screen)
	draw_shield_bar(screen,5,5,player.shield,100)
	draw_lives(screen,WIDTH-80,5,player.lives,mini_player)
	draw_text(screen,str(score),18,WIDTH/2,10)
	draw_shield_bar(screen,5,20,nitr,500)


	#after drawing everythong,flip the display
	pygame.display.flip()

pygame.quit()
