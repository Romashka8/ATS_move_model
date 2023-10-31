# from road_scripts.road import roads
from ats_scripts import ats
import numpy as np


class HumanATS(ats.ATS):
    def __init__(self, position, rm, key):
        super().__init__(position, "Human", rm, key)

    # Находим вероятность перемещения в соседнюю клетку для управляемого человеком АТС.
    # p1, p2, p3 = 0.1, 0.3, 0.95
    # g_max - был опущен.
    def find_p(self, rm):
        dist = self.find_dist(rm)
        try:
            dists = {0: 0, 1: 0.1, 2: 0.3, 3: 0.95}
            return dists[dist]
        except KeyError:
            return 1

    def move(self):
        from road_scripts.road import roads
        rm = roads[self.road_key]
        self.t += 1
        # Кортеж из позиции и типа АТС, не объект класса АТС.
        section = np.random.uniform(0, 1, 10)
        # случай движения (a), (b).
        if np.random.choice(section) <= self.find_p(rm):
            self.moved = 1
            self.move_coord()


class LazyATS(HumanATS):
    def __init__(self, position, rm, key):
        super().__init__(position, rm, key)

    def find_p(self, rm):
        dist = self.find_dist(rm)
        try:
            dists = {0: 0, 1: 0.05, 2: 0.1, 3: 0.3}
            return dists[dist]
        except KeyError:
            return 1
