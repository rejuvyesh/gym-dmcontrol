import pyglet


class Viewer:

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.window = pyglet.window.Window(width=width, height=height, display=None)

    def update(self, pixels):
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        pyglet.image.ImageData(self._width, self._height, 'RGB',
                               pixels.tobytes(), pitch=self._width * -3).blit(0, 0)
        self.window.flip()

    def close(self):
        self.window.close()
