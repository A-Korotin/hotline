from godot import exposed, export
from godot import *


@exposed
class Bat(KinematicBody2D):

	name = export(str)
	
	velocity = export(Vector2)
	
	total_ammo = 0
	current_ammo = 0
	
	def get_total(self):
		return self.total_ammo
		
	def set_total(self, val):
		self.total_ammo = val
		
	def get_current(self):
		return self.current_ammo
		
	def set_current(self, val):
		self.current_ammo = val
		

	def _ready(self):
		self.name = "Bat"

	def attack(self, pos, rot, player):
		for body in player.meleeRange.get_overlapping_bodies():
			if body.is_in_group("enemy"):
				body.die()
		return True

	
	def _physics_process(self, delta):
		if self.velocity != None:
			self.move_and_collide(self.velocity * delta)
			self.velocity -= self.velocity * 2 * delta
