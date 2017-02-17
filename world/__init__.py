class World:
    def __init__(self, name, entities=None):
        self.name = name
        self.entities = entities
        if entities is None:
            self.entities = []

    def update(self):
        for entity in self.entities:
            entity.update()
