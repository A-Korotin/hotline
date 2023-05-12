from godot import exposed, export
from godot import *


@exposed
class Enemy(KinematicBody2D):

	__state_machine = None
	weapon = export(Object)

	def _ready(self):
		self.weapon = None
		self.__state_machine = self.get_node("AnimationTree").get("parameters/playback")
		
	
	def die(self):
		self.__state_machine.travel("Dead")
		self.get_node("CollisionShape2D").disabled = True
