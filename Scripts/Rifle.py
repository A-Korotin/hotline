from godot import exposed, export
from godot import *

from time import time

BULLET_RES = ResourceLoader.load("res://Bullet.tscn")
SOUND_MANAGER_RES = ResourceLoader.load("res://SoundManager.tscn")
SHOT_SOUND = ResourceLoader.load("res://Sounds/Rifle_shot.wav")

@exposed
class Rifle(KinematicBody2D):

	name = export(str)
	
	velocity = export(Vector2)
	
	__bullet_speed = 2_000
	__fire_rate = 0.1

	__can_fire = True
	__prev_fire = time()
	
	total_ammo = 30
	current_ammo = 30
	
	__sound_manager = SOUND_MANAGER_RES.instance()
	
	
	def get_total(self):
		return self.total_ammo
		
	def set_total(self, val):
		self.total_ammo = val
		
	def get_current(self):
		return self.current_ammo
		
	def set_current(self, val):
		self.current_ammo = val
		
	def play_pick_up(self):
		self.__pick_up.play()

	def _ready(self):
		self.name = "Rifle"

	def attack(self, pos, rot, player):
		if self.current_ammo == 0:
			return
		
		if self.__can_fire:
			self.__sound_manager.play_effect(SHOT_SOUND)
			bullet = BULLET_RES.instance()
			bullet.position = pos
			bullet.rotation_degrees = rot / 3.14 * 180
			bullet.velocity = Vector2(self.__bullet_speed, 0).rotated(rot)
			particles = player.find_node("particles")
			particles.emitting = True
			player.get_tree().get_root().call_deferred("add_child", bullet)
			self.__prev_fire = time()
			self.__can_fire = False
			self.current_ammo -= 1
			return True
			
		if time() - self.__prev_fire >= self.__fire_rate:
			self.__can_fire = True
			
		return False
	
	def _physics_process(self, delta):
		if self.velocity != None:
			self.move_and_collide(self.velocity * delta)
			self.velocity -= self.velocity * 2 * delta
