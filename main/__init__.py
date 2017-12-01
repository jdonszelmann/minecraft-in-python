from .window import *
from .chunk import *
import pyglet

w = Window()

event_loop = pyglet.app.EventLoop()
keys = pyglet.window.key.KeyStateHandler()
w.push_handlers(keys)	

def update(dt):
	w.camera.update(dt, keys)


fps = 60

# pyglet.clock.set_fps_limit(fps)
pyglet.clock.schedule_interval(update, 1 / fps)
event_loop.run()
