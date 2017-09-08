# -*- coding:utf-8 -*-
import cocos
import math
from cocos.layer import ColorLayer
from cocos.sprite import Sprite
from cocos.cocosnode import CocosNode
from cocos.director import director
import random
from cocos.actions import MoveTo, CallFuncS
import sys


class Test(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(Test, self).__init__()
        self.speed = 100
        self.color = random.choice(rand_color)
        self.keys_pressed = set()
        self.angle = random.randrange(360)  # 目前角度
        # self.angle = 90
        self.angle_dest = self.angle  # 目标角度
        self.area = Area()
        self.init_dot()
        self.add(self.area)
        self.score = cocos.text.Label('30', font_name='Times New Roman', font_size=24, color=(255, 215, 0, 255))
        self.score.position = 20, 440
        self.add(self.score, 99999)
        self.path = [self.position] * 100
        self.schedule(self.update)

    def init_dot(self):
        for i in range(5):
            self.area.add(Dot())

    def update(self, dt):
        if self.area.snake.head.x > director.get_window_size()[0] or self.area.snake.head.y > director.get_window_size()[1] \
                or self.area.snake.head.x < 14 or self.area.snake.head.y < 14:
            sys.exit()
        self.angle = (self.angle + 360) % 360

        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.area.snake.head.rotation = -self.angle
        self.area.snake.head.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.area.snake.head.y += math.sin(self.angle * math.pi / 180) * dt * self.speed

    def update_score(self):
        self.score.element.text = str(self.area.snake.score)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.move(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)
        self.move(self.keys_pressed)

    def move(self, keys):
        x, y = 0, 0
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


class Area(ColorLayer):
    def __init__(self):
        super(Area, self).__init__(250, 255, 255, 255, director.get_window_size()[0], director.get_window_size()[1])
        self.batch = cocos.batch.BatchNode()
        self.snake = Snake()
        self.add(self.snake)
        self.add(self.batch)


class Dot(Sprite):
    def __init__(self):
        color = random.choice(rand_color)
        super(Dot, self).__init__('img/circle.png', color=color)
        self.position = (random.randint(20, director.get_window_size()[0] - 20),
                         random.randint(20, director.get_window_size()[1] - 20))
        self.is_big = False
        self.scale = 0.8
        self.schedule_interval(self.update, random.random() * 0.2 + 0.1)

    def update(self, dt):
        area = self.parent
        snake = area.snake
        if abs(snake.head.x - self.x) < 20 and abs(snake.head.y - self.y) < 20:
            self.do(MoveTo(snake.position, 0.1) + CallFuncS(self.kill))

    def kill(self, spr):
        spr.unschedule(spr.update)
        arena = spr.parent
        arena.batch.add(Dot())
        arena.snake.add_score()
        # arena.batch.remove(spr)


class Snake(CocosNode):
    def __init__(self):
        super(Snake, self).__init__()
        self.score = 30
        self.head = Sprite('img/circle.png', color=random.choice(rand_color))
        self.head.scale = 1.5
        self.head.set_position(director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
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
        mouth = Sprite('img/circle.png', color=(0, 0, 0))
        mouth.x = +5
        mouth.scale = 0.3
        self.head.add(mouth)
        self.head.add(eye_left)
        self.head.add(eye_right)
        self.add(self.head)
        self.schedule_interval(self.update, random.random() * 0.2 + 0.1)

    def update(self, dt):
        self.parent.parent.update_score()

    def add_score(self, s=1):
        self.score += s


if __name__ == "__main__":
    # print math.sin((180 + 360) % 360 * math.pi / 180)
    # print math.sin(math.radians(180))
    #
    # print math.cos((180 + 360) % 360 * math.pi / 180)
    # print math.cos(math.radians(180))
    #
    rand_color = ((255, 182, 193), (70, 130, 180), (220, 20, 60), (238, 130, 238), (106, 90, 205),
                  (0, 255, 255), (127, 255, 170), (0, 255, 0), (255, 255, 0), (128, 128, 0),
                  (255, 248, 220), (255, 165, 0), (255, 127, 80))
    cocos.director.director.init(caption="coco_snake")
    cocos.director.director.run(cocos.scene.Scene(Test()))
