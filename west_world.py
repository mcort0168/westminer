import time

import states
import items

class BaseGameEntity:
    id = 0

    def __init__(self):
        self.id = BaseGameEntity.id
        BaseGameEntity.id += 1


class Miner(BaseGameEntity):
    """The Miner game object

    """

    def __init__(self, name, current_state, location, gold_carried, gold_bank, thirst, fatigue, build, pickax):
        super(Miner, self).__init__()
        self.name = name
        self.current_state = current_state
        self.location = location
        self.gold_carried = gold_carried
        self.gold_bank = gold_bank
        self.thirst = thirst
        self.fatigue = fatigue
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
            self. strength = 7 + self.pickax.strength

    def update(self):
        self.thirst += 1
        self.current_state.execute(self)

    def change_state(self, new_state):
        self.current_state.exit(self)
        self.current_state = new_state
        self.current_state.enter(self)

    def pockets_full(self):
        if self.gold_carried > self.max_nuggets:
            return True
        else:
            return False

    def thirsty(self):
        if self.thirst > 5:
            return True
        else:
            return False

    def is_tired(self):
        if self.fatigue > 10:
            return True
        else:
            return False
        

if __name__ == '__main__':
    real_miner = Miner('Bob',
                       states.enter_mine_and_dig_for_nugget,
                       'home',
                       0,
                       0,
                       0,
                       0,
                       "bulky",
                       items.small_pickax)
    other_miner = Miner('Sam',
                       states.enter_mine_and_dig_for_nugget,
                       'home',
                       1,
                       10,
                       0,
                       0,
                       "lanky",
                        items.small_pickax)

    game_objects = [real_miner, other_miner]
    counter = 0
    while counter < 50:
        print("Game tick {}".format(counter))
        for obj in game_objects:
            obj.update()
        time.sleep(0.5)
        counter += 1
