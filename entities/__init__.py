class BaseGameEntity:
    id = 0

    def __init__(self, world):
        self.id = BaseGameEntity.id
        BaseGameEntity.id += 1
        self.world = world
