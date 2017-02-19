from . import BaseGameEntity, StateMachine


class Wife(BaseGameEntity):

    def __init__(self, world, name, state_global, state_current, state_previous, location, fatigue, dishes_washed, shirts_ironed, cups_made, lunch_made):
        super(Wife, self).__init__(world)
        self.name = name
        self.location = location
        self.fatigue = fatigue
        self.dishes_washed = dishes_washed
        self.shirts_ironed = shirts_ironed
        self.cups_made = cups_made
        self.max_cups = 2
        self.lunch_made = lunch_made
        self.max_shirts = 3
        state_machine = StateMachine(self, state_global, state_current, state_previous)
        self.state_machine = state_machine

    def update(self):
        self.fatigue += 1
        self.state_machine.update(self)

    def tired(self):
        if self.fatigue > 4:
            return True
        else:
            return False

    def coffee_made(self):
        if self.cups_made == self.max_cups:
            return True
        else:
            return False

    def shirts_clean(self):
        if self.shirts_ironed == self.max_shirts:
            return True
        else:
            return False
