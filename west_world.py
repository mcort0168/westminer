import time
import random
import states
import items


class BaseGameEntity:
    id = 0

    def __init__(self):
        self.id = BaseGameEntity.id
        BaseGameEntity.id += 1


class Plant(BaseGameEntity):
    def __init__(self, location, lifespan):
        super(Plant, self).__init__()
        self.location = location
        self.lifespan = lifespan

    def update(self):
        self.lifespan -= 1
        if self.lifespan == 0:
            self.die()

    def die(self):
        print("A PLANT JUST DIED!!!!")
        game_objects.remove(self)


class PoisonPlant(Plant):
    def __init__(self, location, lifespan, name, condition):
        super(PoisonPlant, self).__init__(location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
            entity.thirst += 4
            entity.fatigue += 4


class EnergyPlant(Plant):
    def __init__(self, location, lifespan, name, condition):
        super(EnergyPlant, self).__init__(location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
        entity.fatigue -= 3


class LiquidPlant(Plant):
    def __init__(self, location, lifespan, name, condition):
        super(LiquidPlant, self).__init__(location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
        entity.thirst -= 3


class UltraPlant(Plant):
    def __init__(self, location, lifespan, name, condition):
        super(UltraPlant, self).__init__(location, lifespan)
        self.name = name
        self.condition = condition

    def effect(self, entity):
        entity.thirst -= 5
        entity.fatigue -= 5


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
        self.max_nuggets = 5
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
        if self.thirst > 10:
            return True
        else:
            return False

    def is_tired(self):
        if self.fatigue > 10:
            return True
        else:
            return False


class Wife(BaseGameEntity):

    def __init__(self, name, wife_state, location, fatigue, dishes_washed, shirts_ironed, cups_made, lunch_made):
        super(Wife, self).__init__()
        self.name=name
        self.wife_state=wife_state
        self.location=location
        self.fatigue=fatigue
        self.dishes_washed=dishes_washed
        self.shirts_ironed=shirts_ironed
        self.cups_made = cups_made
        self.max_cups = 2
        self.lunch_made=lunch_made
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

    miner_wife = Wife('Deloris',
                      states.wake_up_and_make_coffee,
                      'home',
                      0,
                      0,
                      0,
                      0,
                      0)

    game_objects = [real_miner, other_miner, miner_wife]
    counter = 0
    plant_chance = [0, 1, 2, 3, 4, 5]
    while counter < 50:
        print("Game tick {}".format(counter))
        for obj in game_objects:
            obj.update()
        time.sleep(0.5)
        counter += 1
        plant_roll = random.choice(plant_chance)
        if plant_roll == 5 and counter % 5 == 0:
            game_objects.append(PoisonPlant('mine', 30, 'Poison Mushroom', 'Tired and Thirsty'))
            print("This looks safe to eat! Nope, wait, nevermind.".format(real_miner.name))
        if plant_roll in [1, 4] and counter % 3 == 0:
            game_objects.append(EnergyPlant('mine', 30, 'Super Mushroom', 'Energetic'))
            print("I can hear colors now!".format(real_miner.name))
        if plant_roll == 2 and counter % 6 == 0:
            game_objects.append(UltraPlant('mine', 30, 'Star Fruit', 'DANKNESS'))
            print("The fruit of the gods!".format(real_miner.name))
        if plant_roll in [0, 3] and counter % 3 == 0:
            game_objects.append(LiquidPlant('mine', 30, 'Snowbell Flower', 'Soothing'))
            print("How purtty!".format(real_miner.name))
