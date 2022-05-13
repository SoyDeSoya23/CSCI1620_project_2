import pygame 
from laser import Laser


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, constraint, speed):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load('../graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=pos)
		self.speed = speed
		self.max_x_constraint = constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 600

		self.lasers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.05)

		self.can_press = True

	def set_can_press_true(self):
		self.can_press = True

	def set_can_press_false(self):
		self.laser_sound.set_volume(0)
		self.can_press = False

	def get_input(self):
		if self.can_press is True:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_RIGHT]:
				self.rect.x += self.speed
			elif keys[pygame.K_LEFT]:
				self.rect.x -= self.speed

			if keys[pygame.K_SPACE] and self.ready:
				self.shoot_laser()
				self.ready = False
				self.laser_time = pygame.time.get_ticks()
				self.laser_sound.play()
		else:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_RIGHT]:
				self.rect.x = self.rect.x
			elif keys[pygame.K_LEFT]:
				self.rect.x = self.rect.x

			if keys[pygame.K_SPACE] and self.ready:
				# self.shoot_laser()
				self.ready = False
				self.laser_time = pygame.time.get_ticks()
				# self.laser_sound.play()


	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()
