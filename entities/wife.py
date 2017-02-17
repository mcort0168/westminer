from . import BaseGameEntity


class Wife(BaseGameEntity):

    def __init__(self, world, name, wife_state, location, fatigue, dishes_washed, shirts_ironed, cups_made, lunch_made):
        super(Wife, self).__init__(world)
        self.name = name
        self.wife_state = wife_state
        self.location = location
        self.fatigue = fatigue
        self.dishes_washed = dishes_washed
        self.shirts_ironed = shirts_ironed
        self.cups_made = cups_made
        self.max_cups = 2
        self.lunch_made = lunch_made
        self.max_shirts = 3

    def update(self):
        self.fatigue += 1
        self.wife_state.execute(self)

    def wife_change_state(self, new_state):
        self.wife_state.exit(self)
        self.wife_state=new_state
        self.wife_state.enter(self)

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
