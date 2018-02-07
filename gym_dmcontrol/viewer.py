import pyglet


class Viewer:

    def __init__(self, width, height, display=None):
        self._width = width
        self._height = height
        self._display = display
        self.window = None
        self._isopen = False

    def update(self, pixels):
        if self.window is None:
            self.window = pyglet.window.Window(width=self._width, height=self._height,
                                               display=self._display)
            self._isopen = True

        image = pyglet.image.ImageData(self._width, self._height, 'RGB',
                                       pixels.tobytes(), pitch=self._width * -3)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        image.blit(0, 0)
        self.window.flip()

    def close(self):
        if self._isopen:
            self.window.close()
            self._isopen = False

    def __del__(self):
        self.close()
