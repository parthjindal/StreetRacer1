import pygame
import random
import os
from constants import *

game_folder=os.path.dirname(__file__)
imgfolder=os.path.join(game_folder,"img")





class Mob(pygame.sprite.Sprite):
	def __init__(self,speed,i):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig=pygame.image.load(os.path.join(imgfolder,"mob.png")).convert()
		self.image_orig.set_colorkey(BLACK)
		self.image=self.image_orig.copy()
		self.image=pygame.transform.scale(self.image,(100,180))
		self.radius=60

		##self.image=pygame.Surface((30,40))
		##self.image.fill((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
		self.rect=self.image.get_rect()
		#pygame.draw.circle(self.image,GREEN,self.rect.center,self.radius)
		self.rect.x=float(WIDTH*(2*i-1))/(6)
		self.rect.top=0
		self.speedy=-random.randrange(1,3)
		self.relsspeed=self.speedy
		self.speedx=0
		self.i=i

		'''self.rot=0
		self.rot_speed= random.randrange(-20,20)
		self.last_update=pygame.time.get_ticks()'''


	'''def rotate(self):

		now=pygame.time.get_ticks()
		if now - self.last_update>50:
			self.last_update =now
			self.rot=(self.rot+self.rot_speed)%360
			new_image = pygame.transform.rotate(self.image_orig,self.rot)
			old_center=self.rect.center
			self.image=new_image
			self.rect=self.image.get_rect()
			self.rect.center=old_center'''






	def update(self,speed):
		#self.rotate()

		self.relsspeed=self.speedy+speed
		self.rect.y+=self.relsspeed


		if self.rect.top>=HIEGHT or self.rect.left<=0 or self.rect.right>=WIDTH:

			self.rect.top=0
			self.speedy=-random.randrange(3,7)
			self.relsspeed=self.speedy
			#self.image.fill((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
			#q=random.randrange(50,100)
			#self.image_orig=pygame.transform.scale(self.image,(q,q))
		if self.rect.bottom<-HIEGHT:

			self.rect.top=HIEGHT
			self.speedy=-random.randrange(3,7)
			self.relsspeed=self.speedy
