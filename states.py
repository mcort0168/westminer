import random

import items


class State:
    def enter(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError


class EnterMineAndDigForNugget(State):
    def enter(self, miner):
        if miner.location != 'goldmine':
            print("Miner {}: Walkin' to the gold mine.".format(miner.name))
            print("Miner {}: I'm equippin' mah {}".format(miner.name, miner.pickax.name))
            miner.location = 'goldmine'

    def execute(self, miner):
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
            miner.change_state(visit_bank_and_deposit_gold)
        elif miner.thirsty():
            miner.change_state(quench_thirst)

    def exit(self, miner):
        print("Miner {}: Ah'm leavin' the gold mine with mah pockets full o'sweet gold".format(miner.name))


class VisitBankAndDepositGold(State):
    def enter(self, miner):
        if miner.location != 'bank':
            print("Miner {}: Goin' to the bank. Yes siree".format(miner.name))
            miner.location = 'bank'

    def execute(self, miner):
        miner.gold_bank += miner.gold_carried
        miner.gold_carried = 0
        print("Miner {}: Depositin' gold. Total savings now: {}".format(miner.name,
                                                                       miner.gold_bank))
        if miner.gold_bank > 10:
            print("Miner {}: Woohoo! Rich enough for now. Back home to mah li'l lady".format(miner.name))
            miner.change_state(go_home_and_sleep_till_rested)
        elif miner.thirsty():
            miner.change_state(quench_thirst)
        if miner.gold_bank > 50:
            print("Miner {}: Woohoo! Rich enough for now. Back home to mah li'l lady".format(miner.name))
            miner.change_state(go_home_and_sleep_till_rested)
        if miner.gold_bank >= 10:
            if miner.pickax.strength < 3:
                miner.change_state(go_shopping)
            else:
                pass
        if miner.gold_bank >= 15:
            if miner.pickax.strength < 4:
                miner.change_state(go_shopping)
            else:
                pass
        else:
            miner.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        print("Miner {}: Leavin' the bank".format(miner.name))


class GoHomeAndSleepTillRested(State):
    def enter(self, miner):
        if miner.location != 'home':
            print("Miner {}: Going Home to see my lil' lady".format(miner.name))
            miner.location = 'home'

    def execute(self, miner):
        miner.fatigue -= 4
        miner.thirst += 1
        if miner.is_tired():
            miner.change_state(go_home_and_sleep_till_rested)
            print("Miner {}: Just 5 more minutes...".format(miner.name))
            miner.change_state(quench_thirst)
        else:
            miner.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        print("Miner {}: Good mornin'! Another day, another nugget!".format(miner.name))
        

class QuenchThirst(State):
    def enter(self, miner):
        if miner.location != 'saloon':
            print("Miner {}: So thirsty! I'ma go get me a cold one".format(miner.name))
            miner.location = 'saloon'

    def execute(self, miner):
        if miner.gold_carried == 0:
            print("Barkeep: You dirty bum, I'm callin' the sheriff!")
            miner.status = 'arrested'
            miner.change_state(jail)
        else:
            print("Miner {}: That's some fine sippin' liquer.".format(miner.name))
            miner.fatigue += 1
            miner.thirst = 0
            miner.gold_carried -= 1
            print("Miner {}: Whew! That really wet my whistle".format(miner.name))

            if miner.is_tired():
                miner.change_state(go_home_and_sleep_till_rested)
            elif miner.pockets_full():
                miner.change_state(visit_bank_and_deposit_gold)
            else:
                miner.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        if miner.status == 'arrested':
            print("Miner {}: You'll never catch me!".format(miner.name))
        else:
            print("Miner {}: Gotta Get back to it!".format(miner.name))


class Jail(State):
    def enter(self, miner):
        if miner.location != 'jail':
            print("Miner {}: Mama always said I'd end up here".format(miner.name))
            miner.location = 'jail'

    def execute(self, miner):
        miner.fatigue = 0
        miner.thirst = 0
        print("Miner {}: Sittin' in jail".format(miner.name))
        miner.counter_jail += 1
        if miner.counter_jail >= 3:
            miner.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        miner.counter_jail = 0
        miner.status = 'free'
        print("Miner {}: I'm bustin' outta this joint!".format(miner.name))
        print("Miner {}: Gotta Get back to it!".format(miner.name))

class GoShopping(State):
    def enter(self, miner):
        if miner.location != "shop":
            print("Miner {}: Woohoo time to go shoppin' for a new pickax!".format(miner.name))
            miner.location = "shop"

    def execute(self, miner):
        miner.fatigue += 1
        print("Miner {}: Let's see which one should ah' choose?".format(miner.name))
        if miner.gold_bank >= 10:
            if miner.pickax.strength < 3:
                miner.pickax = items.pickax
                print("Miner {}: woohoo I got me a brand spankin' new pickax!".format(miner.name))
                miner.gold_bank -= 10
            else:
                pass
        if miner.gold_bank >= 15:
            if miner.pickax.strength < 4:
                miner.pickax = items.big_pickax
                print("Miner {}: Alrighty I'll be swimmin' in gold now that I got me a big pickax!".format(miner.name))
                miner.gold_bank -= 15
            else:
                pass
        else:
            miner.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        print("Miner {}: Can't wait to try out my new {}".format(miner.name, miner.pickax.name))

class WakeUpAndMakeCoffee(State):
    def enter(self, wife):
        if wife.location != 'home':
            print("{}: Time to make some coffee for my ol' man.".format(wife.name))
            wife.location = 'home'

    def execute(self, wife):
        wife.fatigue += 1
        print ("{}: Coffee keeps me goin' fer my chores.".format(wife.name))
        if wife.coffee_made():
            wife.wife_change_state(wash_dishes)
        if wife.tired():
            wife.wife_change_state(wife_nap)
        else:
            wife.wife_change_state(iron_shirts)

    def exit(self, wife):
        print("{}: That was some delicious breakfast!".format(wife.name))

class WashDishes(State):

    def enter(self, wife):
        print("{}: I tell ya, I made a mess!".format(wife.name))
        wife.location = 'home'

    def execute(self, wife):
        wife.fatigue += 1
        print ("{}: I don't mind washin' these here dishes, anything for my fella.".format(wife.name))
        if wife.dishes_clean():
            wife.wife_change_state(iron_shirts)
        if wife.fatigue():
            wife.wife_change_state(wife_nap)

    def exit(self, wife):
        print("{}: Ah, ain't nothin' better than a clean kitchen".format(wife.name))

class IronShirts(State):

    def enter(self, wife):
        wife.fatigue += 1
        print ("{}: Ole dirty Bob needs some clean, ironed shirts. Diggin' fer nuggets makes'em dirty!".format(wife.name))
        wife.location='home'

    def execute(self, wife):
        print ("{}: Two 'er three shirts will be enough.".format(wife.name))
        if wife.shirts_clean():
            wife.wife_change_state(make_lunch)
        else:
            wife.wife_change_state(wife_nap)

    def exit(self, wife):
        print("{}: Alrighty, Bob will look real nice when he heads to work now!".format(wife.name))

class MakeLunch(State):

    def enter(self, wife):
        wife.fatigue += 1
        print ("{}: Gettin' a lil' hungry. I'm sure Bob would like some lunch too.".format(wife.name))
        wife.location='home'

    def execute(self, wife):
        print("{}: I think some meatloaf sounds right nice!".format(wife.name))
        if wife.lunch_made():
            wife.wife_change_state(wash_dishes)

    def exit(self, wife):
        print ("{}: The day sure is movin' right along.".format(wife.name))

class WifeNap(State):

    def enter(self, wife):
        print("{}: Whew, keepin' up a house is hard work! Time fer a nap".format(wife.name))
        wife.location = 'home'

    def execute(self, wife):
        wife.fatigue -= 0
        if wife.fatigue > 7:
            print("{}: ...zzz...".format(wife.name))
            wife.wife_change_state(wake_up_and_make_coffee)

    def exit(self, wife):
        pass

enter_mine_and_dig_for_nugget = EnterMineAndDigForNugget()
visit_bank_and_deposit_gold = VisitBankAndDepositGold()
go_home_and_sleep_till_rested = GoHomeAndSleepTillRested()
quench_thirst = QuenchThirst()
jail = Jail()
go_shopping = GoShopping()
wake_up_and_make_coffee = WakeUpAndMakeCoffee()
wash_dishes = WashDishes()
wife_nap = WifeNap()
iron_shirts=IronShirts()
make_lunch=MakeLunch()
