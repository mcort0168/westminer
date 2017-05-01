import time
import states
import items
import pygame
from world import World
from entities.miner import Miner
from entities.wife import Wife
from entities import MessageDispatcher


pygame.init()
screen = pygame.display.set_mode((800, 800))
old_map = pygame.image.load("C:/Users/mitoc/Desktop/westminer/World_Map.png")
map = pygame.transform.scale(old_map, (800, 800))
clock = pygame.time.Clock()

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
                   states.go_home_and_sleep_till_rested,
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
                    states.go_home_and_sleep_till_rested,
                    'home',
                    1,
                    10,
                    0,
                    0,
                    "lanky",
                    items.small_pickax)

world.entities.extend([real_miner, other_miner, miner_wife])
world.all_sprite_list.add(real_miner, other_miner)



gameloop = True
counter = 0
WORLDUPDATEEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(WORLDUPDATEEVENT, 400)
while gameloop:
    print("Game tick {}".format(counter))
    counter += 1
    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.QUIT:
            gameloop = False
        if pygame.event.get(WORLDUPDATEEVENT):
            pygame.display.update()
            world.update()
    screen.blit(map, (0,0))
    clock.tick(1)
    world.all_sprite_list.draw(screen)
    world.all_sprite_list.update()
    pygame.display.flip()
    pygame.display.update()


