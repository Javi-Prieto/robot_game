class Wall():
    def __init__(self, sprite, position, size):
        self.position = position
        self.size = size
        self.sprite = sprite
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

class Side_wall(Wall):
    def __init__(self, sprite, position, size, looking_at):
        super().__init__(sprite, position, size)
        self.looking_at = looking_at

