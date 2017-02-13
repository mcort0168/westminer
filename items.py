class Pickax:
    def __init__(self, name, strength, luck, id):
        self.name = name
        self.strength = strength
        self.luck = luck
        self.id = id

old_pickax = Pickax("old pickax", 1, 0, 1)
small_pickax = Pickax("small pickax", 2, 0.01, 2)
pickax = Pickax("pickax", 3, 0.1, 3)
big_pickax = Pickax("big pickax", 4, 0.2, 4)