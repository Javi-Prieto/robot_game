class Player():
    def __init__(self, sprite):
        self.position = [200, 10]
        self.speed = 10
        self.size = [100, 100]
        self.sprite = sprite
        self.life = 10

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def wall_collision(self, wall_position, wall_size):
        if(self.position[0] == wall_position[0] & self.position[1] == wall_position[0]):
            return True
        return False