import pyglet, sys, math, numpy, time, threading, queue, concurrent.futures
from heapq import merge
from itertools import count
from pyglet.gl import *
from .camera import Camera
from .chunk import *
pyglet.options['debug_gl'] = False

class Window(pyglet.window.Window):
	def __init__(self, w=640, h=480, resizable=True, keypressed=0,keyreleased=0, keytyped=0,mousepressed=0,mousedragged = 0,caption="p5.py"):
		super().__init__(w, h, resizable=resizable,caption=caption)
		self.fps_display = pyglet.clock.ClockDisplay()
		self.draw_fps = False

		self.menu = False

		self.set_exclusive_mouse(True)		
		# glShadeModel(GL_SMOOTH)
		glEnable(GL_DEPTH_TEST) 
		glMatrixMode(GL_MODELVIEW)
		glClearColor(0.5,0.7,1.0,1.0)
		gl.glEnable(GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

		glEnable(GL_DEPTH_TEST)
		glClearDepth(1.0)
		glDepthFunc(GL_LEQUAL)
		glEnable(GL_CULL_FACE)

		glEnable(GL_FOG)
		# Set the fog color.
		glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
		# Say we have no preference between rendering speed and quality.
		glHint(GL_FOG_HINT, GL_DONT_CARE)
		# Specify the equation used to compute the blending factor.
		glFogi(GL_FOG_MODE, GL_LINEAR)
		# How close and far away fog starts and ends. The closer the start and end,
		# the denser the fog in the fog range.
		glFogf(GL_FOG_START, 60.0)
		glFogf(GL_FOG_END, 120.0)

		self.camera = Camera(70)
		self.render_distance = 10
		self.c = []
		self.donequeue = queue.Queue()		
		t = threading.Thread(target=self.generate)
		t.daemon = True
		t.start()

	def generate(self):
		def circle_around(x, y):
			yield 0,0
			r = 1
			i, j = x-1, y-1
			while True:
				while i < x+r:
					i += 1
					yield i, j
				while j < y+r:
					j += 1
					yield i, j
				while i > x-r:
					i -= 1
					yield i, j
				while j > y-r:
					j -= 1
					yield i, j
				r += 1
				j -= 1
				yield i, j

		b = time.time()
		with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
			chunks = []
			chunk_gen = []
			for c in circle_around(0,0):
				x,y = c
				if x == self.render_distance/2 or y == self.render_distance/2:
					break
				d = time.time()
				a = chunk(x,y)
				chunk_gen.append(executor.submit(a.generate_mesh))
				chunks.append(a)
			for future,a in zip(concurrent.futures.as_completed(chunk_gen),chunks):
				future.result()
				self.donequeue.put(a)
		print("total time: ", time.time()-b)
		
	def checkgeneratedchunks(self):
		if not self.donequeue.empty():
			a = self.donequeue.get()
			a.make_mesh()
			self.c.append(a)

	def cls(self):
		self.clear()
		# pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

	@property
	def size(self):
		return Vector(self.get_size())

	@property
	def width(self):
		return self.get_size()[0]

	@property
	def height(self):
		return self.get_size()[1]

	def resize(self,w,h):
		self.set_size(w,h)

	def on_close(self):
		self.close()
		sys.exit()

	def on_draw(self):
		self.cls()
		self.camera.draw()
		#draw fps onscreen - dev option
		if self.draw_fps:
			self.fps_display.draw()
		print(pyglet.clock.get_fps())

		self.checkgeneratedchunks()

		glPushMatrix()

		glEnable(GL_TEXTURE_2D)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		# glRotatef(self.xRotation, 1, 0, 0)
		# glRotatef(self.yRotation, 0, 1, 0)
		# glRotatef(self.zRotation, 0, 0, 1)
		for i in self.c:
			i.batch.draw()
		# Pop Matrix off stack
		glPopMatrix()

	def on_resize(self, width, height):
		# set the Viewport
		glViewport(0, 0, width, height)

		# using Projection mode
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		aspectRatio = width / height
		gluPerspective(35, aspectRatio, 1, 1000)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslatef(0, 0, -400)


	def on_mouse_motion(self,x, y, dx, dy):
		if not self.menu:
			self.camera.yaw(dx)
			self.camera.pitch(dy)

	def on_mouse_press(self,x, y, button, modifiers):
		pass

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			self.menu = not self.menu
			self.set_exclusive_mouse(not self.menu)
		
		if symbol == pyglet.window.key.Q:
			self.on_close()

	def on_key_release(self, symbol, modifiers):
		pass


