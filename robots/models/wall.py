class Wall():
    def __init__(self, sprite, position, size):
        self.position = position
        self.size = size
        self.sprite = sprite


class Side_wall(Wall):
    def __init__(self, sprite, position, size, looking_at):
        super().__init__(sprite, position, size)
        self.looking_at = looking_at
