class Player():
    def __init__(self, sprite):
        self.position = [10, 10]
        self.speed = 10
        self.size = [100, 100]
        self.sprite = sprite

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed
