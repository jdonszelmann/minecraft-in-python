import numpy, pyglet, os, time
from .util import *
from . import noise
from .shader import Shader
from pyglet.gl import *
path = os.path.dirname(os.path.abspath(__file__))
seed = 5

texturedb = {}

texturepaths = {
	0:None,
	1: "main/textures/textures/blocks/stone.png",
	2: "main/textures/textures/blocks/dirt.png",
}

elevation = noise.noise(seed)
roughness = noise.noise(seed+1)
detail = noise.noise(seed+2)

class chunk:
	def __init__(self,x,z):
		self.x = x
		self.z = z
		self.init_shader()
		self.batch = pyglet.graphics.Batch()
		self.width = 16
		self.height = 255
		self.depth = 16
		self.blocks = numpy.zeros((self.width+2,self.height,self.depth+2))
		self.faces = numpy.zeros((self.width,self.height,self.depth))

	def generate_heightmap(self):
		for x in range(self.blocks.shape[0]):
			for z in range(self.blocks.shape[2]):
				x_t = x + self.x*(self.width) - self.x*2
				z_t = z - self.z*(self.depth) + self.z*2
				rand = (elevation.noise2d(x_t*0.0005,z_t*0.0005) + (roughness.noise2d(x_t*0.005,z_t*0.005)*detail.noise2d(x_t*0.1,z_t*0.1)))*64+64
				# rand = elevation.noise2d(x_t*0.01,z_t*0.01)*64+64
				a = numpy.zeros((255))
				a[0:int(rand)] = 1
				a[int(rand):int(rand) + 2 + abs(int(detail.noise2d(x_t*0.01,z_t*0.01)*8))] = 2
				self.blocks[x,:,z] = a

	def init_shader(self):
		vertex_shader = ""
		fragment_shader = ""

		with open("main/shaders/world.vert") as handle:
			vertex_shader = handle.read()

		with open("main/shaders/world.frag") as handle:
			fragment_shader = handle.read()

		self.shader = Shader([vertex_shader], [fragment_shader])

	def start_shader(self):
		self.shader.bind()

	def stop_shader(self):
		self.shader.unbind()

	def generate_mesh(self):
		self.generate_heightmap()
		lastsolid = False
		for y in range(self.blocks.shape[1]-1,0,-1):
			thissolid = True
			if not lastsolid and not numpy.sum(self.blocks[:,y,:]) == 0:
				for x in range(self.blocks.shape[0]):
					for z in range(self.blocks.shape[2]):
						face = 63
						if x > 0 and self.blocks[x-1,y,z] != 0: #assuming 0 = air
							face -= 1
						if x < self.blocks.shape[0] - 1 and self.blocks[x+1,y,z] != 0: #assuming 0 = air
							face -= 2
						if y > 0 and self.blocks[x,y-1,z] != 0: #assuming 0 = air
							face -= 4
						if y < self.blocks.shape[1] - 1 and self.blocks[x,y+1,z] != 0: #assuming 0 = air
							face -= 8
						if z > 0 and self.blocks[x,y,z-1] != 0: #assuming 0 = air
							face -= 16
						if z < self.blocks.shape[2] - 1 and self.blocks[x,y,z+1] != 0: #assuming 0 = air
							face -= 32

						if self.blocks[x,y,z] == 0:
							thissolid = False

						if self.blocks[x,y,z] != 0 and face != 0 and x > 1 and x < self.blocks.shape[0]-2 and z > 1 and z < self.blocks.shape[2]-2:
							vertices = cube_vertices(x+(self.x * self.width)-self.x*2, y, z-(self.z * self.depth)+self.z*2, 0.5,face)
							vertice_num = int(len(vertices)/3)
							shade_data = cube_shade(1, 1, 1, 1, face)
							coords = 	[	0.0,0.0,
											1.0,0.0, 
											1.0,1.0,
											0.0,1.0
										]*int(vertice_num/4)
							colors = [255,0,0]*vertice_num
							t = texture(self.blocks[x,y,z])
							self.batch.add(vertice_num, pyglet.gl.GL_QUADS,t,
								('v3f',vertices),
								('c3f', shade_data),
								('t2f',coords),
							)				
				lastsolid = thissolid

class texture(pyglet.graphics.TextureGroup):
	def __init__(self, number):
		global texturedb
		if number not in texturedb.keys():
			texturedb.update({number:pyglet.image.load(texturepaths[number]).get_texture()})
		
		super().__init__(texturedb[number])







