def cube_vertices(x, y, z, n, faces):
	"""Return the vertices of the cube at position x, y, z with size 2*n."""

	data = '{0:06b}'.format(int(faces))
	a = []

	if data[2] == "1":
		a += [ x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n] #top
	if data[3] == "1":
		a += [ x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n] #bottom
	if data[5] == "1" :
		a += [ x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n] #left
	if data[4] == "1":
		a += [ x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n] #right
	if data[0] == "1":
		a += [ x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n] #front
	if data[1] == "1":
		a += [ x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n] #back
	return a


def cube_shade(x, y, z, n, faces):
	"""Return the color diference between the sides of the cube."""

	data = '{0:06b}'.format(int(faces))
	a = []

	if data[2] == "1":
		a += [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] #top
	if data[3] == "1":
		a += [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3] #bottom
	if data[5] == "1" :
		a += [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] #left
	if data[4] == "1":
		a += [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8] #right
	if data[0] == "1":
		a += [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] #front
	if data[1] == "1":
		a += [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8] #back
	return a