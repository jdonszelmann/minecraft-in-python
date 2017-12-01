import pyglet, math
from pyglet.gl import *

class Camera:
	movement_speed = 15.0
	mouse_sensitivity = 0.25
	y_inv = False
	dx=dy=0

	key_map = {
		'forward': pyglet.window.key.W,
		'backward': pyglet.window.key.S,
		'left': pyglet.window.key.A,
		'right': pyglet.window.key.D,
		'up': pyglet.window.key.SPACE,
		'down': pyglet.window.key.LSHIFT
	}

	def __init__(self, y = 0):
		self.__position = [0,-y,0]
		self.__yaw = 0.0
		self.__pitch = 0.0

	def move_forward(self, distance):
		"""Move forward on distance"""
		self.__position[0] -= distance * math.sin(math.radians(self.__yaw))
		self.__position[2] += distance * math.cos(math.radians(self.__yaw))

	def move_backward(self, distance):
		"""Move backward on distance"""
		self.__position[0] += distance * math.sin(math.radians(self.__yaw))
		self.__position[2] -= distance * math.cos(math.radians(self.__yaw))

	def move_left(self, distance):
		"""Move left on distance"""
		self.__position[0] -= distance * math.sin(math.radians(self.__yaw - 90))
		self.__position[2] += distance * math.cos(math.radians(self.__yaw - 90))

	def move_right(self, distance):
		"""Move right on distance"""
		self.__position[0] -= distance * math.sin(math.radians(self.__yaw + 90))
		self.__position[2] += distance * math.cos(math.radians(self.__yaw + 90))	

	def move_up(self, distance):
		"""Move up on distance"""
		self.__position[1] -= distance

	def move_down(self, distance):
		"""Move down on distance"""
		self.__position[1] += distance

	def yaw(self, yaw):
		"""Turn above x-axis"""
		self.__yaw += yaw * self.mouse_sensitivity

	def pitch(self, pitch):
		"""Turn above y-axis"""
		self.__pitch += pitch * self.mouse_sensitivity * ((1) if self.y_inv else -1)

		if(self.__pitch > 90):
			self.__pitch = 90
		if(self.__pitch < -90):
			self.__pitch= -90

	def update(self,dt, keys):	

		if keys[self.key_map['forward']]:
			self.move_forward(dt * self.movement_speed)

		if keys[self.key_map['backward']]:
			self.move_backward(dt * self.movement_speed)

		if keys[self.key_map['left']]:
			self.move_left(dt * self.movement_speed)

		if keys[self.key_map['right']]:
			self.move_right(dt * self.movement_speed)

		if keys[self.key_map['up']]:
			self.move_up(dt * self.movement_speed)

		if keys[self.key_map['down']]:
			self.move_down(dt * self.movement_speed)

	def draw(self):
		"""Apply transform"""
		glLoadIdentity()
		pyglet.gl.glRotatef(self.__pitch, 1.0, 0.0, 0.0)
		pyglet.gl.glRotatef(self.__yaw, 0.0, 1.0, 0.0)
		pyglet.gl.glTranslatef(*self.__position)