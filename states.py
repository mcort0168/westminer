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
        print("Miner {}: Depostin' gold. Total savings now: {}".format(miner.name,
                                                                       miner.gold_bank))
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
            print("Miner {}: Just 5 more minutes...".format(miner.name)) #new dialogue
        if miner.thirsty():
            miner.change_state(quench_thirst) #changed from 'go_home_and_sleep_till_rested' to 'quench_thirst'.
        else:
            miner.change_state(enter_mine_and_dig_for_nugget)

    def exit(self, miner):
        print("Miner {}: Good mornin'! Another day, another nugget!".format(miner.name)) #updated miner exit dialogue
        

class QuenchThirst(State):
    def enter(self, miner):
        if miner.location != 'saloon':
            print("Miner {}: So thirsty! Ima go get me cold one".format(miner.name))
            miner.location = 'saloon'

    def execute(self, miner):
        miner.fatigue += 1
        miner.thirst -= 3
        print("Miner {}: That's some fine sippin' liquor.".format(miner.name))
        if miner.thirsty():
            miner.change_state(quench_thirst)
        if miner.pockets_full():
            miner.change_state(visit_bank_and_deposit_gold)
        if miner.is_tired():
            miner.change_state(go_home_and_sleep_till_rested)
        else:
            print("Miner {}: Whew! That really wet my wistle".format(miner.name))
            miner.change_state(enter_mine_and_dig_for_nugget) #changed visit_bank_and_deposit_gold to enter_mine_and_dig_for_nugget

    def exit(self, miner):
        print("Miner {}: Gotta Get back to it!".format(miner.name))

class GoShopping(State):
    def enter(self,miner):
        if miner.location != "shop":
            print("Miner {}: Woohoo time to go shoppin' for a new pickax!".format(miner.name))
            miner.location = "shop"

    def execute(self,miner):
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

    def exit(self,miner):
        print("Miner {}: Can't wait to try out my new {}".format(miner.name, miner.pickax.name))

enter_mine_and_dig_for_nugget = EnterMineAndDigForNugget()
visit_bank_and_deposit_gold = VisitBankAndDepositGold()
go_home_and_sleep_till_rested = GoHomeAndSleepTillRested()
quench_thirst = QuenchThirst()
go_shopping = GoShopping()
