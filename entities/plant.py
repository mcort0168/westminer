from . import BaseGameEntity, StateMachine


class Plant(BaseGameEntity):
    def __init__(self, world, state_global, state_current, state_previous, location, lifespan):
        super(Plant, self).__init__(world)
        self.location = location
        self.lifespan = lifespan
        state_machine = StateMachine(self, state_global, state_current, state_previous)
        self.state_machine = state_machine

    def update(self):
        self.lifespan -= 1
        if self.lifespan == 0:
            self.die()

    def die(self):
        print("A PLANT JUST DIED!!!!")
        self.world.entities.remove(self)


class PoisonPlant(Plant):
    def __init__(self, world, state_global, state_current, state_previous, location, lifespan, name, condition):
        super(PoisonPlant, self).__init__(world, state_global, state_current, state_previous, location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
            entity.thirst += 4
            entity.fatigue += 4


class EnergyPlant(Plant):
    def __init__(self, world, state_global, state_current, state_previous, location, lifespan, name, condition):
        super(EnergyPlant, self).__init__(world, state_global, state_current, state_previous, location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
        entity.fatigue -= 3


class LiquidPlant(Plant):
    def __init__(self, world, state_global, state_current, state_previous, location, lifespan, name, condition):
        super(LiquidPlant, self).__init__(world, state_global, state_current, state_previous, location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
        entity.thirst -= 3


class UltraPlant(Plant):
    def __init__(self, world, state_global, state_current, state_previous, location, lifespan, name, condition):
        super(UltraPlant, self).__init__(world, state_global, state_current, state_previous, location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
        entity.thirst -= 5
        entity.fatigue -= 5
