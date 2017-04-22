import time
import random
import states
import items
import pygame
from world import World
from entities.miner import Miner
from entities.wife import Wife
from entities.plant import PoisonPlant, EnergyPlant, UltraPlant, LiquidPlant
from entities import MessageDispatcher

pygame.init()
screen = pygame.display.set_mode((800, 800))
old_map = pygame.image.load("C:/Users/mitoc/Desktop/westminer/World_Map.png")
map = pygame.transform.scale(old_map, (800, 800))

gameloop = True
while gameloop:
    counter = 0
    for event in pygame.event.get():
        counter += 1
        if event.type == pygame.QUIT:
            gameloop = False
    screen.blit(map, (0,0))

    if __name__ == '__main__':
        world = World('westworld')
        dispatcho = MessageDispatcher(world)

        miner_wife = Wife(world,
                          'Deloris',
                          states.wife_global,
                          states.wake_up_and_make_coffee,
                          states.wake_up_and_make_coffee,
                          'home',
                          0,
                          0,
                          0,
                          0,
                          False)
        real_miner = Miner(world,
                           'Bob',
                           states.enter_mine_and_dig_for_nugget,
                           states.enter_mine_and_dig_for_nugget,
                           states.enter_mine_and_dig_for_nugget,
                           'home',
                           0,
                           0,
                           0,
                           0,
                           "bulky",
                           items.small_pickax,
                           miner_wife)
        miner_wife.husband = real_miner
        other_miner = Miner(world,
                            'Sam',
                            states.enter_mine_and_dig_for_nugget,
                            states.enter_mine_and_dig_for_nugget,
                            states.enter_mine_and_dig_for_nugget,
                            'home',
                            1,
                            10,
                            0,
                            0,
                            "lanky",
                            items.small_pickax)

        world.entities.extend([real_miner, other_miner, miner_wife])
        world.all_sprite_list.add(real_miner)
        world.all_sprite_list.draw(screen)
        world.all_sprite_list.update()

        pygame.display.flip()
        plant_chance = [0, 1, 2, 3, 4, 5]
        print("Game tick {}".format(counter))
        world.dispatcher.dispatch_delayed()
        world.update()
        time.sleep(0.5)

        plant_roll = random.choice(plant_chance)
        if plant_roll == 5 and counter % 5 == 0:
            world.entities.append(PoisonPlant(world,
                                              None, None, None,
                                              'mine',
                                              30,
                                              'Poison Mushroom',
                                              'Tired and Thirsty'))
        if plant_roll in [1, 4] and counter % 3 == 0:
            world.entities.append(EnergyPlant(world,
                                              None, None, None,
                                              'mine',
                                              30,
                                              'Super Mushroom',
                                              'Energetic'))
        if plant_roll == 2 and counter % 6 == 0:
            world.entities.append(UltraPlant(world,
                                             None, None, None,
                                             'mine',
                                             30,
                                             'Star Fruit',
                                             'DANKNESS'))
        if plant_roll in [0, 3] and counter % 3 == 0:
            world.entities.append(LiquidPlant(world,
                                              None, None, None,
                                              'mine',
                                              30,
                                              'Snowbell Flower',
                                              'Soothing'))
