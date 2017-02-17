import time
import random
import states
import items
from world import World
from entities.miner import Miner
from entities.wife import Wife
from entities.plant import PoisonPlant, EnergyPlant, UltraPlant, LiquidPlant


if __name__ == '__main__':
    world = World('westworld')

    real_miner = Miner(world,
                       'Bob',
                       states.enter_mine_and_dig_for_nugget,
                       'home',
                       0,
                       0,
                       0,
                       0,
                       "bulky",
                       items.small_pickax)
    other_miner = Miner(world,
                        'Sam',
                        states.enter_mine_and_dig_for_nugget,
                        'home',
                        1,
                        10,
                        0,
                        0,
                        "lanky",
                        items.small_pickax)

    miner_wife = Wife(world,
                      'Deloris',
                      states.wake_up_and_make_coffee,
                      'home',
                      0,
                      0,
                      0,
                      0,
                      0)
    world.entities.extend([real_miner, other_miner, miner_wife])
    counter = 0
    plant_chance = [0, 1, 2, 3, 4, 5]
    while counter < 50:
        print("Game tick {}".format(counter))
        world.update()
        time.sleep(0.5)
        counter += 1
        plant_roll = random.choice(plant_chance)
        if plant_roll == 5 and counter % 5 == 0:
            world.entities.append(PoisonPlant(world, 'mine', 30, 'Poison Mushroom', 'Tired and Thirsty'))
            print("This looks safe to eat! Nope, wait, nevermind.".format(real_miner.name))
        if plant_roll in [1, 4] and counter % 3 == 0:
            world.entities.append(EnergyPlant(world, 'mine', 30, 'Super Mushroom', 'Energetic'))
            print("I can hear colors now!".format(real_miner.name))
        if plant_roll == 2 and counter % 6 == 0:
            world.entities.append(UltraPlant(world, 'mine', 30, 'Star Fruit', 'DANKNESS'))
        if plant_roll in [0, 3] and counter % 3 == 0:
            world.entities.append(LiquidPlant(world, 'mine', 30, 'Snowbell Flower', 'Soothing'))
