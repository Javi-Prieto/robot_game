class Wall():
    def __init__(self, sprite, position, size):
        self.position = position
        self.size = size
        self.sprite = sprite
        self.hitbox = (self.position[0], self.position[1], self.size[0], self.size[1])

