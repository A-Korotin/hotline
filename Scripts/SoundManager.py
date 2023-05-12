from godot import exposed, export
from godot import *


@exposed
class SoundManager(Node):

	def play_effect(self, effect):
		n = self.get_child_count()
		for i in range(n):
			child = self.get_child(i)
			if not child.is_playing():
				child.set_stream(effect)
				child.play(0)
				return
