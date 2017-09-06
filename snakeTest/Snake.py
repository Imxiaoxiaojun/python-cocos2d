# -*- coding:utf-8 -*-
import cocos
import math
from cocos.sprite import Sprite
import random


class Snake(cocos.cocosnode.CocosNode):
    def __init__(self, is_enemy=False):
        super(Snake, self).__init__()
        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度
        self.color = random.choice(((255, 182, 193), (70, 130, 180), (220, 20, 60), (238, 130, 238), (106, 90, 205),
                                   (0, 255, 255), (127, 255, 170), (0, 255, 0), (255, 255, 0), (128, 128, 0),
                                   (255, 248, 220), (255, 165, 0), (255, 127, 80)))
        if is_enemy:
            self.position = random.randrange(300, 1300), random.randrange(200, 600)
            if 600 < self.x < 1000:
                self.x += 400
        else:
            self.position = random.randrange(700, 900), random.randrange(350, 450)
        self.is_enemy = is_enemy
        self.head = Sprite('img/circle.png', color=self.color)
        self.scale = 1.5
        self.init_head()
        self.speed = 150
        self.score = 30
        self.length = 3
        self.body = []

        if not is_enemy:
            self.speed = 180
        self.path = [self.position] * 100

        self.schedule(self.update)

        # if self.is_enemy:
        #     self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)

    def init_head(self):
        # eyeball = Sprite('img/circle.png', color=(0, 0, 0))
        eyeball = Sprite('img/circle.png', color=(253, 55, 80))
        eyeball.scale = 0.5

        eye_left = Sprite('img/circle.png')
        eye_left.x = 5
        eye_left.scale = 0.5
        eye_left.add(eyeball)

        eye_right = Sprite('img/circle.png')
        eye_right.x = -5
        eye_right.scale = 0.5
        eye_right.add(eyeball)

        self.head.add(eye_left)
        self.head.add(eye_right)
        self.add(self.head)

    def init_body(self):
        for i in range(self.length):
            self.add_body()

    def add_body(self):
        b = Sprite('img/circle.png', color=self.color)
        b.scale = 1.5
        self.body.append(b)
        if self.x == 0:
            print self.position
        b.position = self.position
        self.parent.batch.add(b, 9999 - len(self.body))

    def update(self, dt):
        self.angle = (self.angle + 360) % 360

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed
        self.path.append(self.position)
        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.head.rotation = -self.angle

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed
        self.path.append(self.position)

        lag = int(round(1100.0 / self.speed))
        for i in range(int(self.length)):
            idx = (i + 1) * lag + 1
            self.body[i].position = self.path[-min(idx, len(self.path))]
            if self.body[i].x == 0:
                print(self.body[i].position)
        m_l = max(self.length * lag * 2, 60)
        if len(self.path) > m_l:
            self.path = self.path[int(-m_l * 2):]

    def update_angle(self, keys):
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
    cocos.director.director.run(cocos.scene.Scene(Snake()))
