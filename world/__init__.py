import pygame


class World:
    def __init__(self, name, entities=None):
        self.name = name
        self.entities = entities
        if entities is None:
            self.entities = []

    all_sprite_list = pygame.sprite.Group()

    def update(self):
        for entity in self.entities:

            entity.update()
            pygame.display.update()


    def get_entity(self, eid):
        return next((entity for entity in self.entities
                     if entity.eid == eid),
                    None)

    def remove_entity(self, eid):
        entity = self.get_entity(eid)
        if entity is not None:
            self.entities.pop(self.entities.index(entity))
            return entity
        return entity

