# -*- coding:utf-8 -*-
import cocos
from Area import Area


class BootStrap(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(BootStrap, self).__init__()
        self.score = cocos.text.Label('30', font_name='Times New Roman', font_size=24, color=(255, 215, 0, 255))
        self.score.position = 20, 440
        self.add(self.score, 99999)
        self.arena = Area()
        self.add(self.arena)

    def update_score(self):
        self.score.element.text = str(self.arena.snake.score)

    def on_mouse_press(self, x, y, buttons, modifiers):
        print x, y, buttons


if __name__ == "__main__":
    cocos.director.director.init(caption="coco_snake")
    scene1 = cocos.scene.Scene(BootStrap())
    cocos.director.director.run(scene1)
