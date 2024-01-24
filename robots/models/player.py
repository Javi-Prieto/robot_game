from robots.models.wall import Wall


class Player():
    def __init__(self, sprite):
        self.position = [100, 60]
        self.speed = 1
        self.size = [70, 70]
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

    def wall_collision(self, wall: Wall):
        match wall.looking_at:
            case 0:
                if self.position[1] <= wall.position[1] + wall.size[1]:
                    return True
            case 1:
                if self.position[1] >= wall.position[1] - wall.size[1]:
                    return True
            case 2:
                if self.position[0] <= wall.position[0] + wall.size[0]:
                    return True
            case 3:
                if self.position[0] >= wall.position[0] - wall.size[0]:
                    return True
            case _:
                return False
        return False
