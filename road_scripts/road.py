# в классе Road используется паттерн MonoState.
import numpy as np


# только для однополосного движения!
class Road:
    def __init__(self, cells=10):
        self._cells = cells
        self._road = np.zeros(self._cells, dtype="int8")

    def __repr__(self):
        return f"Road(cells={self._cells})"

    # fill_cell и clear_cell используются при моделировании движения.
    # проверка на допустимость очистки/заполнения клетки происходит в ATS.move_coord().
    def fill_cell(self, coord, ats_type):
        self._road[coord] = 1 if ats_type == "Human" else 2

    def clear_cell(self, coord):
        self._road[coord] = 0

    def get_free_cells(self):
        return np.array(np.where(self._road == 0))[0]

    def get_fill_cells(self):
        return np.array(np.where(self._road > 0))[0]

    def get_cells(self):
        return self._cells

    def get_road(self):
        return self._road

    # Убрать все АТС с дороги.
    def clear_road(self):
        self._road = np.zeros(self._cells, dtype="int8")


# для возможности проводить параллельные вычисления.
def roads_dict(roads_count, roads_size=10):
    return dict(zip((i for i in range(roads_count)), (Road(roads_size) for i in range(roads_count))))


roads = roads_dict(5, 100)
