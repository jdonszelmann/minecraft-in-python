import main

w = main.Window()

event_loop = pyglet.app.EventLoop()

def update(dt):
	pass

pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule_interval(update, 1 / Globals.FPS)
event_loop.run()

