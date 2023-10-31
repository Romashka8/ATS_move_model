from road_scripts.road import roads


class ATS:
    # таблица всех АТС на дороге.
    _all_ats = {}

    # rm - объект класса Road из road.py
    def __init__(self, position, ats_type, rm, key):
        self.position = position if position in rm.get_free_cells() else rm.get_free_cells()[0]
        self.ats_type = ats_type if ats_type in ("Human", "Robot") else "Human"
        # дорога, к которой относится АТС.
        self.road_key = key
        # ближайший АТС - объект класса АТС.
        self.closest_ats = None
        ATS._all_ats[f"ATS({self.position}, {self.ats_type})"] = self
        # пройденный АТС путь.
        self.s = 0
        # Время АТС в движении с момента запуска модели.
        self.t = 0
        self.moved = 0
        rm.fill_cell(self.position, self.ats_type)

    def __del__(self):
        del self

    def __repr__(self):
        return f"ATS({self.position}, {self.ats_type})"

    def set_moved(self):
        self.moved = 1

    def reset_moved(self):
        self.moved = 0

    # Ищет координаты ближайшего АТС и определяет его тип.
    def find_closest_ats(self, rm):
        cells = rm.get_fill_cells()
        road = rm.get_road()
        if cells[cells > self.position].any():
            pos = cells[cells > self.position][0]
            ats_type = "Human" if road[pos] == 1 else "Robot"
            self.closest_ats = ATS._all_ats[f"ATS({pos}, {ats_type})"]
            return
        if cells[cells <= self.position].any():
            pos = cells[cells <= self.position][0]
            ats_type = "Human" if road[pos] == 1 else "Robot"
            self.closest_ats = ATS._all_ats[f"ATS({pos}, {ats_type})"]
            return

    # Ищет расстяние до ближайшего АТС.
    def find_dist(self, rm):
        cells = rm.get_cells()
        if self.position < self.closest_ats.position:
            # if self.position != 0:
            return self.closest_ats.position - self.position - 1
            # return self.closest_ats.position - 2
        if self.position > self.closest_ats.position:
            return cells - self.position + self.closest_ats.position - 1
        return cells - 1

    # Перемешение координат АТС.
    def move_coord(self):
        rm = roads[self.road_key]
        free_cells = rm.get_free_cells()
        changed_pos = self.position + 1
        if changed_pos in free_cells:
            rm.fill_cell(changed_pos, self.ats_type)
            rm.clear_cell(self.position)
            self.position += 1
            self.s += 1
            return
        if changed_pos == rm.get_cells() and 0 in free_cells:
            rm.fill_cell(0, self.ats_type)
            rm.clear_cell(self.position)
            self.position = 0
            self.s += 1
            return

    # ищем скорость АТС в момент времени.
    def find_speed(self):
        return self.s / self.t if self.t != 0 else 0

    def get_position(self):
        return self.position

    # Определяется в наследниках.
    def move(self):
        pass
