from . import BaseGameEntity, StateMachine
import pygame


class Miner(BaseGameEntity,  pygame.sprite.Sprite):
    """The Miner game object

    """

    def __init__(self, world, name, state_global, state_current, state_previous, location, gold_carried, gold_bank, thirst, fatigue, build, pickax, wife=None):
        super(Miner, self).__init__(world)
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load("miner/minerback.png")
        self.rect = self.image.get_rect()
        self.old_location = ""
        self.location = location
        self.new_location = ""
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
        self.wife = wife

    def update(self):
        self.thirst += 1
        self.state_machine.update(self)
        pygame.display.flip()

    def handle_message(self, telegram):
        self.state_machine.handle_message(telegram)

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
