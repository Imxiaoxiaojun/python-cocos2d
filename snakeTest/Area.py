# -*- coding:utf-8 -*-
import cocos
from cocos.director import director
from Dot import Dot
from Snake import Snake


class Area(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        # super(Area, self).__init__(250, 255, 255, 255, 1600, 800)
        super(Area, self).__init__(250, 255, 255, 255, director.get_window_size()[0], director.get_window_size()[1])
        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
        self.batch = cocos.batch.BatchNode()
        self.add(self.batch)

        for i in range(5):
            self.batch.add(Dot())

        self.snake = Snake()
        self.add(self.snake, 9999)
        self.snake.init_body()

        # self.enemies = []
        # for i in range(7):
        #     self.add_enemy()

        self.keys_pressed = set()

        self.schedule(self.update)

    def update(self, dt):
        pass
        # self.x = self.center[0] - self.snake.x
        # self.y = self.center[1] - self.snake.y

    def add_enemy(self):
        enemy = Snake(True)
        self.add(enemy, 10000)
        enemy.init_body()
        self.enemies.append(enemy)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.snake.update_angle(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)
        self.snake.update_angle(self.keys_pressed)


if __name__ == "__main__":
    cocos.director.director.init(caption="coco_snake")
    cocos.director.director.run(cocos.scene.Scene(Area()))
