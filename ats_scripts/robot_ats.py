from ats_scripts import ats
# from road_scripts.road import roads


class RobotATS(ats.ATS):
    # Указывается вручную перед запуском эксперимента.
    cluster = True
    _max_cluster_size = 4
    delayed = []

    def __init__(self, position, rm, key):
        super().__init__(position, "Robot", rm, key)


    def move(self):
        from road_scripts.road import roads
        rm = roads[self.road_key]
        self.t += 1
        if not RobotATS.cluster:
            self.moved = 1
            self.move_coord()
            return
        self._move_cl(rm)

    def _move_cl(self, rm):
        if self.moved == 1:
            return
        dist = self.find_dist(rm)
        if dist <= 0:
            RobotATS.delayed.append(self)
            self.moved = 1
            return
        if dist >= 1 or self.closest_ats.ats_type == "Human":
            self.moved = 1
            RobotATS.delayed.append(self)
            RobotATS.delayed = (RobotATS.delayed[::-1])[:RobotATS._max_cluster_size]
            list(map(RobotATS.move_coord, RobotATS.delayed))
            RobotATS.delayed = []
            return
