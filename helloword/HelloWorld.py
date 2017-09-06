import cocos
from cocos.director import director
import pyglet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class KeyDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(KeyDisplay, self).__init__()

        self.text = cocos.text.Label('Keys: ', font_size=18, x=100, y=280)
        self.add(self.text)

        self.keys_pressed = set()

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        self.text.element.text = 'Keys: ' + ','.join(key_names)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)
        self.update_text()


class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.text = cocos.text.Label('Mouse @', font_size=18,
                                     x=100, y=240)
        self.add(self.text)

    def on_mouse_motion(self, x, y, dx, dy):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)
        self.text.element.x, self.text.element.y = director.get_virtual_coordinates(x, y)


director.init(resizable=True)
main_scene = cocos.scene.Scene( KeyDisplay(), MouseDisplay() )
director.run(main_scene)
