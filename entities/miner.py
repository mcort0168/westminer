from . import BaseGameEntity, StateMachine


class Miner(BaseGameEntity):
    """The Miner game object

    """

    def __init__(self, world, name, state_global, state_current, state_previous, location, gold_carried, gold_bank, thirst, fatigue, build, pickax):
        super(Miner, self).__init__(world)
        self.name = name
        self.location = location
        self.gold_carried = gold_carried
        self.gold_bank = gold_bank
        self.thirst = thirst
        self.fatigue = fatigue
        self.status = 'free'
        self.counter_jail = 0
        self.max_nuggets = 7
        self.pickax = pickax
        if build == "lanky":
            self.health = 30
            self.strength = 3 + self.pickax.strength
        if build == "normal":
            self.health = 50
            self.strength = 5 + self.pickax.strength
        if build == "bulky":
            self.health = 70
            self.strength = 7 + self.pickax.strength
        state_machine = StateMachine(self, state_global, state_current, state_previous)
        self.state_machine = state_machine

    def update(self):
        self.thirst += 1
        self.state_machine.update(self)

    def pockets_full(self):
        if self.gold_carried > self.max_nuggets:
            return True
        else:
            return False

    def thirsty(self):
        if self.thirst > 10:
            return True
        else:
            return False

    def is_tired(self):
        if self.fatigue > 10:
            return True
        else:
            return False
