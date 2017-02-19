class BaseGameEntity:
    eid = 0

    def __init__(self, world):
        self.eid = BaseGameEntity.eid
        BaseGameEntity.eid += 1
        self.world = world


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
        self.state_current = new_state
        self.state_current.enter(self.entity)

    def update(self, entity):
        self.state_current.execute(entity)
