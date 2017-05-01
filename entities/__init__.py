from datetime import datetime
import heapq
import pygame

import travel
from travel import traveling

class BaseGameEntity:
    eid = 0

    def __init__(self, world):
        self.eid = BaseGameEntity.eid
        BaseGameEntity.eid += 1
        self.world = world

    def handle_message(self, telegram):
        raise NotImplementedError


class StateMachine:
    def __init__(self, entity, state_global, state_current, state_previous=None):
        self.entity = entity
        self.state_global = state_global
        self.state_current = state_current
        self.state_previous = state_previous

    def revert(self):
        new_previous = self.state_current
        self.state_current = self.state_previous
        self.state_previous = new_previous

    def change_state(self, new_state):
        self.state_current.exit(self.entity)
        self.state_previous = self.state_current
        self.state_current = new_state
        #traveling(self.entity, self.state_previous, self.state_current)
        self.state_current.enter(self.entity)


    def update(self, entity, telegram=None):
        self.state_current.execute(entity)
        if telegram is not None:
            self.handle_message(telegram)

    def handle_message(self, telegram):
        if self.state_current is not None and self.state_current.handler:
            self.state_current.on_message(self.entity, telegram)
        elif self.state_global is not None and self.state_global.handler:
            self.state_global.on_message(self.entity, telegram)


class Telegram:
    def __init__(self, sender, receiver, msg, dispatch_time=None, **kwargs):
        self.sender = sender
        self.receiver = receiver
        self.msg = msg
        self.dispatch_time = dispatch_time


class MessageDispatcher:
    def __init__(self, world):
        self.world = world
        self.world.dispatcher = self
        self.priorityQ = []

    def discharge(self, receiver, telegram):
        receiver.state_machine.handle_message(telegram)

    def dispatch(self, delay, sender, receiver, msg, **kwargs):
        telegram = Telegram(sender, receiver, msg, **kwargs)
        if isinstance(delay, int):
            if delay <= 0:
                self.discharge(receiver, telegram)
        else:
            telegram.dispatch_time = datetime.now() + delay
            heapq.heappush(self.priorityQ, telegram)

    def dispatch_delayed(self):
        if self.priorityQ:
            current_time = datetime.now()
            next_message = self.priorityQ[0]
            while next_message.dispatch_time <= current_time:
                next_telegram = heapq.heappop(self.priorityQ)
                self.discharge(next_telegram.receiver, next_telegram)
                if self.priorityQ:
                    current_time = datetime.now()
                    next_message = self.priorityQ[0]
                else:
                    next_message = Telegram(None, None, None, datetime.max)
