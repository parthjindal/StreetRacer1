import pygame
import random
import os 

game_folder=os.path.dirname(__file__)
imgfolder=os.path.join(game_folder,"img")





class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(os.path.join(imgfolder,"laserRed16.png")).convert()
		self.rect=self.image.get_rect()
		self.rect.bottom=y
		self.rect.centerx=x
		self.speedy=-10
		self.now=pygame.time.get_ticks()

	def update(self):

		self.rect.y+=self.speedy
		##kill if out
		if self.rect.bottom<0:
			self.kill()

