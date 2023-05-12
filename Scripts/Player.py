from godot import exposed, export
from godot import *



@exposed
class Player(KinematicBody2D):
	
	__ms = 500
	__throw_speed = 1000
	__pick_up_area = None
	meleeRange = export(Object)
	__state_machine = None
	weapon = export(Object)

	def _ready(self):
		self.weapon = None
		self.__pick_up_area = self.get_node("pickup_shape")
		self.meleeRange = self.get_node("MeleeRange")
		self.__state_machine = self.get_node("AnimationTree").get("parameters/playback")
		pass
		
	def __get_input(self):
		direction = Vector2()
		
		if Input.is_action_pressed("up"):
			direction.y -= 1.0
		if Input.is_action_pressed("down"):
			direction.y += 1.0
		if Input.is_action_pressed("left"):
			direction.x -= 1.0
		if Input.is_action_pressed("right"):
			direction.x += 1.0 
		
		return direction.normalized()
		
	
	
	def _physics_process(self, delta):
		direction = self.__get_input()
		direction = self.move_and_slide(direction * self.__ms)
		self.look_at(self.get_global_mouse_position())
		
		animation = "walk" if direction != Vector2.ZERO else "idle"
		weapon = self.weapon.name if self.weapon != None else "Hand"
		
		if Input.is_action_pressed("pick_up"):
			self.__pick_up()
		if Input.is_action_pressed("RMB"):
			self.__throw()
		if Input.is_action_pressed("LMB"):
			self.__attack()
			return
					
		current = str(self.__state_machine.get_current_node())
		if 'attack' not in current:
			self.__state_machine.travel(f"{weapon}_{animation}")
		

		
	
	def __pick_up(self):	
		if self.weapon != None:
			return
			
		for body in self.__pick_up_area.get_overlapping_bodies():
			if body.is_in_group("weapon"):
				self.weapon = body.duplicate()
				self.weapon.set_current(body.get_current())
				body.call_deferred("free")
				break
				
	def __throw(self):
		if self.weapon == None:
			return
		
		node = self.weapon
		ammo = self.weapon.get_current()
		self.weapon = None
		
		node.position = self.get_global_position()
		node.rotation_degrees = self.rotation_degrees
		node.velocity = Vector2(self.__throw_speed, 0).rotated(self.rotation)
		
		self.get_tree().get_root().call_deferred("add_child", node)
		node.set_current(ammo)
	
	def __fist_attack(self):
		for body in self.meleeRange.get_overlapping_bodies():
			if body.is_in_group("enemy"):
				body.die()
		
	def __attack(self):
		weapon = self.weapon.name if self.weapon != None else "Hand"
		
		
		success = True
		
		if self.weapon != None:
			success = self.weapon.attack(self.find_node("Bullet point").get_global_position(), self.rotation, self)
		else:
			self.__fist_attack()
			
		if success:
			self.__state_machine.travel(f"{weapon}_attack")
			
			
	def die(self):
		self.__state_machine.travel("Dead")
		self.get_node("CollisionShape2D").disabled = True
		
			
		
