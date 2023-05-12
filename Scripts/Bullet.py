from godot import exposed, export
from godot import *

from time import time

@exposed
class Bullet(KinematicBody2D):

	velocity = export(Vector2)
	
	__start_time = None
	__TTL = 1
	
	def _ready(self):
		self.__start_time = time()

	def _physics_process(self, delta):
		if time() - self.__start_time > self.__TTL:
			self.queue_free()
		collision = self.move_and_collide(self.velocity * delta)
		
		if collision:
			self.queue_free()
			if collision.collider.is_in_group("enemy"):
				collision.collider.die()
			
		
