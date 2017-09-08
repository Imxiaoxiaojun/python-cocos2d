# -*- coding:utf-8 -*-
import random
from cocos.actions import MoveTo, CallFuncS
from cocos.director import director
from cocos.sprite import Sprite


class Dot(Sprite):
    def __init__(self, pos=None, color=None):
        if color is None:
            color = random.choice(((255, 182, 193), (70, 130, 180), (220, 20, 60), (238, 130, 238), (106, 90, 205),
                                   (0, 255, 255), (127, 255, 170), (0, 255, 0), (255, 255, 0), (128, 128, 0),
                                   (255, 248, 220), (255, 165, 0), (255, 127, 80)))

        super(Dot, self).__init__('img/circle.png', color=color)
        self.killed = False
        if pos is None:
            # self.position = (random.randint(40, 1600 - 40), random.randint(40, 800 - 40))
            self.position = (random.randint(40, director.get_window_size()[0] - 40), random.randint(40, director.get_window_size()[1] - 40))
            self.is_big = False
            self.scale = 0.8
        else:
            self.position = (pos[0] + random.random() * 32 - 16, pos[1] + random.random() * 32 - 16)
            self.is_big = True
        self.schedule_interval(self.update, random.random() * 0.2 + 0.1)

    def update(self, dt):
        arena = self.parent.parent
        snake = arena.snake
        self.check_kill(snake)

    def kill(self, spr):
        spr.unschedule(spr.update)
        arena = spr.parent.parent
        if not spr.is_big:
            arena.batch.add(Dot())
            spr.killer.add_score()
        else:
            spr.killer.add_score(2)
        arena.batch.remove(spr)
        if not spr.killer.is_enemy:
            arena.parent.update_score()
        del spr

    def check_kill(self, snake):
        if (not self.killed) and (abs(snake.x - self.x) < 32 and abs(snake.y - self.y) < 32):
            self.killed = True
            self.killer = snake
            self.do(MoveTo(snake.position, 0.1) + CallFuncS(self.kill))
        # print self.color, snake
