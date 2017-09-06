# -*- coding:utf-8 -*-
import cocos
import math
from cocos.layer import ColorLayer
from cocos.sprite import Sprite
from cocos.cocosnode import CocosNode
from cocos.director import director
import random
import sys


class Test(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(Test, self).__init__()
        self.color = random.choice(((255, 182, 193), (70, 130, 180), (220, 20, 60), (238, 130, 238), (106, 90, 205),
                                    (0, 255, 255), (127, 255, 170), (0, 255, 0), (255, 255, 0), (128, 128, 0),
                                    (255, 248, 220), (255, 165, 0), (255, 127, 80)))
        self.area = ColorLayer(250, 255, 255, 255, director.get_window_size()[0], director.get_window_size()[1])
        # self.batch = cocos.batch.BatchNode()
        # self.add(self.batch)

        self.snake = CocosNode()

        self.head = Sprite('img/circle.png', color=self.color)
        self.head.scale = 1.5
        self.head.set_position(director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)

        self.dot = Sprite('img/circle.png', color=self.color)
        self.dot.position = (random.randint(20, director.get_window_size()[0] - 20),
                        random.randint(20, director.get_window_size()[1] - 20))
        self.dot.is_big = False
        self.dot.scale = 0.8

        eyeball = Sprite('img/circle.png', color=(253, 55, 80))
        eyeball.scale = 0.5

        eye_left = Sprite('img/circle.png')
        eye_left.y = 5
        eye_left.scale = 0.5
        eye_left.add(eyeball)

        eye_right = Sprite('img/circle.png')
        eye_right.y = -5
        eye_right.scale = 0.5
        eye_right.add(eyeball)

        self.head.add(eye_left)
        self.head.add(eye_right)

        self.keys_pressed = set()

        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度

        self.snake.add(self.head)

        self.area.add(self.snake)
        self.area.add(self.dot)
        self.add(self.area)
        self.path = [self.position] * 100
        self.schedule(self.update)
        self.schedule_interval(self.update2, random.random() * 0.2 + 0.1)

    def update2(self, dt):
        print dt

    def update(self, dt):
        if self.head.x > director.get_window_size()[0] or self.head.y > director.get_window_size()[1]\
                or self.head.x < 14 or self.head.y < 14:
            sys.exit()
        self.angle = (self.angle + 360) % 360
        self.head.x += math.cos(self.angle * math.pi / 180) * dt * 180
        self.head.y += math.sin(self.angle * math.pi / 180) * dt * 180
        self.path.append(self.position)
        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.head.rotation = -self.angle

        self.head.x += math.cos(self.angle * math.pi / 180) * dt * 180
        self.head.y += math.sin(self.angle * math.pi / 180) * dt * 180
        self.path.append(self.position)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.move(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)
        self.move(self.keys_pressed)

    def move(self, keys):
        x, y = 0, 0
        print keys
        if 65361 in keys:  # 左
            x -= 1
        if 65362 in keys:  # 上
            y += 1
        if 65363 in keys:  # 右
            x += 1
        if 65364 in keys:  # 下
            y -= 1
        directs = ((225, 180, 135), (270, None, 90), (315, 0, 45))
        direct = directs[x + 1][y + 1]
        if direct is None:
            self.angle_dest = self.angle
        else:
            self.angle_dest = direct


if __name__ == "__main__":
    cocos.director.director.init(caption="coco_snake")
    cocos.director.director.run(cocos.scene.Scene(Test()))
