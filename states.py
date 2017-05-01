from datetime import datetime, timedelta
import random
import pygame

import world
import items
import images

class State:
    def __init__(self, handler=False):
        self.handler = handler

    def enter(self, entity):
        raise NotImplementedError

    def execute(self, entity):
        raise NotImplementedError

    def exit(self, entity):
        raise NotImplementedError


class EnterMineAndDigForNugget(State):
    def __init__(self, handler=False):
        super(EnterMineAndDigForNugget, self).__init__(handler=handler)

    def enter(self, miner):
        if miner.location != 'goldmine':
            print("Miner {}: Walkin' to the gold mine.".format(miner.name))
            print("Miner {}: I'm equippin' mah {}".format(miner.name, miner.pickax.name))
            miner.location = 'goldmine'

    def execute(self, miner):
        miner.image = images.mine
        miner.rect.x = 400
        miner.rect.y = 0
        r = random.random() - miner.pickax.luck
        if r < 0.25:
            miner.gold_carried += 4
            miner.fatigue += 1
            miner.thirst += 1
            print("Miner {}: 4 nuggets!!Hit the jackpot boyhowdy!!".format(miner.name))
        elif r < 0.50:
            miner.gold_carried += 2
            miner.fatigue += 1
            miner.thirst += 1
            print("Miner {}: 2 nuggets!! Yeehaw thats not a bad amount of nuggets for a days work.".format(miner.name))
        elif r < 0.95:
            miner.gold_carried += 1
            miner.fatigue += 1
            miner.thirst += 1
            print("Miner {}: Pickin' up a nugget".format(miner.name))

        else:
            miner.fatigue += 1
            miner.thirst += 1
            print("Miner {}: NO NUGGETS!? I'm gonna be here all day at this rate".format(miner.name))

        if miner.pockets_full():
            miner.state_machine.change_state(traveling)
            miner.new_location = "bank"
        elif miner.thirsty():
            miner.state_machine.change_state(traveling)
            miner.new_location = "saloon"

    def exit(self, miner):
        print("Miner {}: Ah'm leavin' the gold mine with mah pockets full o'sweet gold".format(miner.name))
        miner.old_location = "goldmine"


class VisitBankAndDepositGold(State):
    def __init__(self, handler=False):
        super(VisitBankAndDepositGold, self).__init__(handler=handler)

    def enter(self, miner):
        if miner.location != 'bank':
            print("Miner {}: Goin' to the bank. Yes siree".format(miner.name))
            miner.location = 'bank'

    def execute(self, miner):
        miner.image = images.deposit
        miner.rect.x = 455
        miner.rect.y = 600
        miner.gold_bank += miner.gold_carried
        miner.gold_carried = 0
        print("Miner {}: Depositin' gold. Total savings now: {}".format(miner.name,
                                                                       miner.gold_bank))
        if miner.gold_bank > 10:
            print("Miner {}: Woohoo! Rich enough for now. Back home to mah li'l lady".format(miner.name))
            miner.state_machine.change_state(traveling)
            miner.new_location = "home"
        elif miner.thirsty():
            miner.state_machine.change_state(traveling)
            miner.new_location = "saloon"
        if miner.gold_bank > 50:
            print("Miner {}: Woohoo! Rich enough for now. Back home to mah li'l lady".format(miner.name))
            miner.state_machine.change_state(traveling)
            miner.new_location = "home"
        if miner.gold_bank >= 10:
            if miner.pickax.strength < 3:
                miner.state_machine.change_state(traveling)
                miner.new_location = "shop"
            else:
                pass
        if miner.gold_bank >= 15:
            if miner.pickax.strength < 4:
                miner.state_machine.change_state(traveling)
                miner.new_location = "shop"
            else:
                pass
        else:
            miner.state_machine.change_state(traveling)
            miner.new_location = "goldmine"

    def exit(self, miner):
        print("Miner {}: Leavin' the bank".format(miner.name))
        miner.old_location = "bank"


class GoHomeAndSleepTillRested(State):
    def __init__(self, handler=False):
        super(GoHomeAndSleepTillRested, self).__init__(handler=handler)

    def enter(self, miner):
        if miner.location != 'home':
            miner.location = 'home'
            miner.image = images.sleep
            miner.rect.x = 400
            miner.rect.y = 784
            if miner.wife is not None:
                print("Miner {}: Going Home to see my lil' lady".format(miner.name))
                miner.world.dispatcher.dispatch(0, miner, miner.wife, 'HiHoneyImHome')
            else:
                print("Miner {}: Going Home!".format(miner.name))

    def execute(self, miner):
        miner.fatigue -= 4
        miner.thirst += 1
        if miner.is_tired():
            miner.state_machine.change_state(go_home_and_sleep_till_rested)
            print("Miner {}: Just 5 more minutes...".format(miner.name))
            miner.new_location = "home"
        elif miner.thirsty():
            miner.state_machine.change_state(quench_thirst)
            miner.new_location = "saloon"
        else:
            miner.state_machine.change_state(enter_mine_and_dig_for_nugget)
            miner.new_location = "goldmine"

    def exit(self, miner):
        print("Miner {}: Good mornin'! Another day, another nugget!".format(miner.name))
        miner.old_location = "home"


class QuenchThirst(State):
    def __init__(self, handler=False):
        super(QuenchThirst, self).__init__(handler=handler)

    def enter(self, miner):
        if miner.location != 'saloon':
            print("Miner {}: So thirsty! I'ma go get me a cold one".format(miner.name))
            miner.location = 'saloon'

    def execute(self, miner):
        if miner.gold_carried == 0:
            miner.image = images.drink
            miner.rect.x = 360
            miner.rect.y = 500
            print("Barkeep: You dirty bum, I'm callin' the sheriff!")
            miner.status = 'arrested'
            miner.state_machine.change_state(jail)
            miner.new_location = "jail"
        else:
            print("Miner {}: That's some fine sippin' liquer.".format(miner.name))
            miner.fatigue += 1
            miner.thirst = 0
            miner.gold_carried -= 1
            print("Miner {}: Whew! That really wet my whistle".format(miner.name))

            if miner.is_tired():
                miner.state_machine.change_state(traveling)
                miner.new_location = "home"
            elif miner.pockets_full():
                miner.state_machine.change_state(traveling)
                miner.new_location = "goldmine"
            else:
                miner.state_machine.change_state(traveling)
                miner.new_location = "goldmine"

    def exit(self, miner):
        miner.old_location = "saloon"
        if miner.status == 'arrested':
            print("Miner {}: You'll never catch me!".format(miner.name))
        else:
            print("Miner {}: Gotta Get back to it!".format(miner.name))


class Jail(State):
    def __init__(self, handler=False):
        super(Jail, self).__init__(handler=handler)

    def enter(self, miner):
        if miner.location != 'jail':
            print("Miner {}: Mama always said I'd end up here".format(miner.name))
            miner.location = 'jail'

    def execute(self, miner):
        miner.fatigue = 0
        miner.thirst = 0
        miner.image = images.jail
        miner.rect.x = 455
        miner.rect.y = 450
        print("Miner {}: Sittin' in jail".format(miner.name))
        miner.counter_jail += 1
        if miner.counter_jail >= 3:
            miner.state_machine.change_state(traveling)
            miner.new_location = "goldmine"

    def exit(self, miner):
        miner.counter_jail = 0
        miner.status = 'free'
        print("Miner {}: I'm bustin' outta this joint!".format(miner.name))
        print("Miner {}: Gotta Get back to it!".format(miner.name))
        miner.old_location = "jail"


class GoShopping(State):
    def __init__(self, handler=False):
        super(GoShopping, self).__init__(handler=handler)

    def enter(self, miner):
        print("Miner {}: Woohoo time to go shoppin' for a new pickax!".format(miner.name))
        miner.location = "shop"

    def execute(self, miner):
        miner.fatigue += 1
        miner.image = False
        miner.image = images.deposit
        miner.rect.x = 360
        miner.rect.y = 630
        print("Miner {}: Let's see which one should ah' choose?".format(miner.name))
        if miner.gold_bank >= 10:
            if miner.pickax.strength < 3:
                miner.pickax = items.pickax
                print("Miner {}: woohoo I got me a brand spankin' new pickax!".format(miner.name))
                miner.gold_bank -= 10
                miner.state_machine.change_state(traveling)
                miner.new_location = "goldmine"
            else:
                miner.state_machine.change_state(traveling)
                miner.new_location = "goldmine"
        elif miner.gold_bank >= 15:
            if miner.pickax.strength < 4:
                miner.pickax = items.big_pickax
                print("Miner {}: Alrighty I'll be swimmin' in gold now that I got me a big pickax!".format(miner.name))
                miner.gold_bank -= 15
                miner.state_machine.change_state(traveling)
                miner.new_location = "goldmine"
            else:
                miner.state_machine.change_state(traveling)
                miner.new_location = "goldmine"
        else:
            miner.state_machine.change_state(traveling)
            miner.new_location = "goldmine"

    def exit(self, miner):
        print("Miner {}: Can't wait to try out my new {}".format(miner.name, miner.pickax.name))
        miner.old_location = "shop"


class Traveling(State):
    def __init__(self, handler=False):
        super(Traveling, self).__init__(handler=handler)

    def enter(self, miner):
        miner.location = "traveling"
        print("Miner {}: Time to stretch mah legs!".format(miner.name))

    def execute(self, miner):
        if miner.old_location == "goldmine":
            miner.rect.y = 32
            miner.rect.x = 400
            miner.image = images.miner_front
            if miner.new_location == "bank":
                while miner.rect.y != 600:
                    miner.rect.y += 1
                    pygame.display.update()
                    if miner.rect.y == 600:
                        miner.image = images.miner_right
                        miner.state_machine.change_state(visit_bank_and_deposit_gold)
            if miner.new_location == "saloon":
                while miner.rect.y != 500:
                    pygame.display.update()
                    miner.rect.y += 1
                    if miner.rect.y == 500:
                        miner.image = images.miner_left
                        miner.state_machine.change_state(quench_thirst)
        if miner.old_location == "bank":
            miner.rect.y = 600
            miner.rect.x = 442
            miner.image = images.miner_left
            if miner.new_location == "goldmmine":
                miner.image = images.miner_front
                while miner.rect.y != 784:
                    pygame.display.update()
                    miner.rect.y += 1
                    if miner.rect.y == 784:
                        miner.image = images.sleep
                        miner.state_machine.change_state(go_home_and_sleep_till_rested)
            if miner.new_location == "saloon":
                miner.image = images.miner_back
                while miner.rect.y != 500:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 500:
                        miner.image = images.miner_left
                        miner.state_machine.change_state(quench_thirst)
            if miner.new_location == "shop":
                miner.image = images.miner_left
                while miner.rect.x != 376:
                    pygame.display.update()
                    miner.rect.x -= 1
                    if miner.rect.x == 376:
                        miner.state_machine.change_state(go_shopping)
            if miner.new_location == "goldmine":
                while miner.rect.y != 24:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 24:
                        miner.state_machine.change_state(enter_mine_and_dig_for_nugget)
        if miner.old_location == "home":
            miner.rect.y = 784
            miner.rect.x = 400
            miner.image = images.miner_back
            if miner.new_location == "saloon":
                while miner.rect.y != 500:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 500:
                        miner.image = images.miner_left
                        miner.state_machine.change_state(quench_thirst)
            if miner.new_location == "goldmine":
                while miner.rect.y != 24:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 24:
                        miner.state_machine.change_state(enter_mine_and_dig_for_nugget)
        if miner.old_location == "saloon":
            miner.rect.y = 500
            miner.rect.x = 376
            miner.image = images.miner_right
            if miner.new_location == "jail":
                miner.image = images.miner_back
                while miner.rect.y != 450:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 450:
                        miner.image = images.miner_right
                        miner.state_machine.change_state(jail)
            if miner.new_location == "home":
                miner.image = images.miner_front
                while miner.rect.y != 784:
                    pygame.display.update()
                    miner.rect.y += 1
                    if miner.rect.y == 784:
                        miner.state_machine.change_state(go_home_and_sleep_till_rested)
            if miner.new_location == "bank":
                miner.image = images.miner_front
                while miner.rect.y != 600:
                    pygame.display.update()
                    miner.rect.y += 1
                    if miner.rect.y == 600:
                        miner.image = images.miner_right
                        miner.state_machine.change_state(visit_bank_and_deposit_gold)
            if miner.new_location == "goldmine":
                miner.image = images.miner_back
                while miner.rect.y != 24:
                    miner.rect.y -= 1
                    if miner.rect.y == 24:
                        miner.state_machine.change_state(enter_mine_and_dig_for_nugget)
        if miner.old_location == "jail":
            miner.rect.y = 450
            miner.rect.x = 442
            miner.image = images.miner_left
            if miner.new_location == "goldmine":
                miner.image = images.miner_back
                while miner.rect.y != 24:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 24:
                        miner.state_machine.change_state(enter_mine_and_dig_for_nugget)
        if miner.old_location == "shop":
            miner.rect.y = 630
            miner.rect.x = 344
            miner.image = images.miner_right
            if miner.new_location == "goldmine":
                miner.image = images.miner_back
                while miner.rect.y != 24:
                    pygame.display.update()
                    miner.rect.y -= 1
                    if miner.rect.y == 24:
                        miner.state_machine.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        print("Miner {}: I'm here!".format(miner.name))
        miner.location = miner.new_location
        miner.new_location = ""

class WakeUpAndMakeCoffee(State):
    def __init__(self, handler=False):
        super(WakeUpAndMakeCoffee, self).__init__(handler=handler)

    def enter(self, wife):
        if wife.location != 'home':
            print("{}: Time to make some coffee for my ol' man.".format(wife.name))
            wife.location = 'home'

    def execute(self, wife):
        wife.fatigue += 1
        print ("{}: Coffee keeps me goin' fer my chores.".format(wife.name))
        if wife.coffee_made():
            wife.state_machine.change_state(wash_dishes)
        if wife.tired():
            wife.state_machine.change_state(wife_nap)
        else:
            wife.state_machine.change_state(iron_shirts)

    def exit(self, wife):
        print("{}: That was some delicious breakfast!".format(wife.name))


class WashDishes(State):
    def __init__(self, handler=False):
        super(WashDishes, self).__init__(handler=handler)

    def enter(self, wife):
        print("{}: I tell ya, I made a mess!".format(wife.name))
        wife.location = 'home'

    def execute(self, wife):
        wife.fatigue += 1
        print("{}: I don't mind washin' these here dishes, anything for my fella.".format(wife.name))
        if wife.dishes_clean():
            wife.state_machine.change_state(iron_shirts)
        if wife.fatigue():
            wife.state_machine.change_state(wife_nap)

    def exit(self, wife):
        print("{}: Ah, ain't nothin' better than a clean kitchen".format(wife.name))


class IronShirts(State):
    def __init__(self, handler=False):
        super(IronShirts, self).__init__(handler=handler)

    def enter(self, wife):
        wife.fatigue += 1
        print("{}: Ole dirty Bob needs some clean, ironed shirts. Diggin' fer nuggets makes'em dirty!".format(wife.name))
        wife.location='home'

    def execute(self, wife):
        print("{}: Two 'er three shirts will be enough.".format(wife.name))
        if wife.shirts_clean():
            wife.state_machine.change_state(make_lunch)
        else:
            wife.state_machine.change_state(wife_nap)

    def exit(self, wife):
        print("{}: Alrighty, Bob will look real nice when he heads to work now!".format(wife.name))


class MakeLunch(State):
    def __init__(self, handler=True):
        super(MakeLunch, self).__init__(handler=handler)

    def enter(self, wife):
        wife.location = 'home'
        if not wife.cooking:
            wife.fatigue += 1
            print("{}: Puttin' the stew in the oven.".format(wife.name))
            print("STEW MESSAGE SENT AT {}".format(datetime.now()))
            wife.world.dispatcher.dispatch(timedelta(seconds=5), wife, wife, 'StewReady')
            wife.cooking = True

    def execute(self, wife):
        print("{}: Waitin on this stew!".format(wife.name))
        # if wife.lunch_made():
        #     wife.state_machine.change_state(wash_dishes)

    def exit(self, wife):
        print("{}: The day sure is movin' right along.".format(wife.name))

    def on_message(self, wife, telegram):
        if telegram.msg == 'StewReady':
            print("Message received by {} at {}".format(wife.name, datetime.now()))
            print("Stew ready! Let's eat!")
            wife.world.dispatcher.dispatch(0, wife, wife.husband, 'StewReady')
            wife.cooking = False
            wife.state_machine.change_state(iron_shirts)


class WifeNap(State):
    def __init__(self, handler=False):
        super(WifeNap, self).__init__(handler=handler)

    def enter(self, wife):
        print("{}: Whew, keepin' up a house is hard work! Time fer a nap".format(wife.name))
        wife.location = 'home'

    def execute(self, wife):
        wife.fatigue -= 0
        if wife.fatigue > 7:
            print("{}: ...zzz...".format(wife.name))
            wife.state_machine.change_state(wake_up_and_make_coffee)

    def exit(self, wife):
        pass


class WifeGlobalState(State):
    def __init__(self, handler=True):
        super(WifeGlobalState, self).__init__(handler=handler)

    def on_message(self, entity, telegram):
        if telegram.msg == 'HiHoneyImHome':
            print("Message handled by {} at {}".format(entity.name, datetime.now()))
            print("Hi honey.  Let me make you some of mah fine country stew!")
            entity.state_machine.change_state(make_lunch)

enter_mine_and_dig_for_nugget = EnterMineAndDigForNugget()
visit_bank_and_deposit_gold = VisitBankAndDepositGold()
go_home_and_sleep_till_rested = GoHomeAndSleepTillRested()
quench_thirst = QuenchThirst()
jail = Jail()
go_shopping = GoShopping()
traveling = Traveling()
wake_up_and_make_coffee = WakeUpAndMakeCoffee()
wash_dishes = WashDishes()
wife_nap = WifeNap()
iron_shirts = IronShirts()
make_lunch = MakeLunch()
wife_global = WifeGlobalState()

