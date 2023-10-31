from road_scripts.road import roads
from road_scripts import traffic as tr
from ats_scripts.human_ats import HumanATS, LazyATS
from ats_scripts.robot_ats import RobotATS
import road_scripts.v
import numpy as np
import shelve
import sys

sys.setrecursionlimit(10000)


# all_ats - счётчик всех АТС на дороге.
# concentrate - концентрация управляемых человеком АТС на дороге.
# key - дорога, к которой привязаны АТС.
def generate_arrays(all_ats, concentrate, key, lazy):
    h_ats_count = int(round(all_ats * concentrate))
    r_ats_count = all_ats - h_ats_count
    l_ats_concentrate = 0.8
    l_ats_count = int(h_ats_count * l_ats_concentrate)
    l_arr = []
    # добавление в поток "ленивых" АТС.
    if lazy:
        l_arr = [LazyATS(np.random.choice(roads[key].get_free_cells()), roads[key], key) for i in range(l_ats_count)]
        h_ats_count -= l_ats_count
    h_arr = [HumanATS(np.random.choice(roads[key].get_free_cells()), roads[key], key) for i in range(h_ats_count)]
    h_arr = tr.insert_sort(h_arr + l_arr)
    r_arr = tr.generate_r_ats(r_ats_count, roads[key], key)
    for i in r_arr:
        i.find_closest_ats(roads[key])
    for i in h_arr:
        i.find_closest_ats(roads[key])
    return h_arr, r_arr


# t - время стабилизации.
# h_arr, r_arr - массивы АТС.
def rec_stab(t, h_arr, r_arr):
    if t == 0:
        return
    list(map(HumanATS.move, h_arr))
    r_arr = tr.check_head(r_arr)
    list(map(RobotATS.move, r_arr))
    list(map(RobotATS.reset_moved, r_arr))
    #
    list(map(HumanATS.reset_moved, h_arr))
    rec_stab(t - 1, h_arr, r_arr)


# НЕ ЗАБУДЬ ПОСЧИТАТЬ P!
# И V тоже.
def rec_stat(t, h_arr, r_arr):
    if t == 0:
        return
    list(map(HumanATS.move, h_arr))
    r_arr = tr.check_head(r_arr)
    list(map(RobotATS.reset_moved, r_arr))
    #
    list(map(HumanATS.reset_moved, h_arr))
    list(map(RobotATS.move, r_arr))
    road_scripts.v.increase_v(sum(list(map(HumanATS.find_speed, h_arr))))
    road_scripts.v.increase_v(sum(list(map(RobotATS.find_speed, r_arr))))
    rec_stat(t - 1, h_arr, r_arr)


def proc_do(h_arr, r_arr):
    list(map(HumanATS.move, h_arr))
    r_arr = tr.check_head(r_arr)
    list(map(RobotATS.move, r_arr))
    road_scripts.v.increase_v(sum(list(map(HumanATS.find_speed, h_arr))))
    road_scripts.v.increase_v(sum(list(map(RobotATS.find_speed, r_arr))))


def proc_reset(h_arr, r_arr):
    list(map(RobotATS.reset_moved, r_arr))
    list(map(HumanATS.reset_moved, h_arr))


# key - общее число АТС на дороге, должен быть строкой.
# path - буть к .bin файлу.
# rm - объект класса Road.
# h_arr, r_arr - массивы АТС, прикреплённых к rm.
def save_conf(key, path, rm, h_arr, r_arr):
    data = (rm, h_arr, r_arr)
    with shelve.open(path) as file:
        file[key] = data
    return


# key - общее число АТС на дороге, должен быть строкой.
# path - буть к .bin файлу.
def load_conf(key, path):
    with shelve.open(path) as file:
        data = file[key]
    return data


def save_stat(p, v, path):
    with open(path, "a") as file:
        file.write(str(p) + " " + str(p * v) + "\n")


# сохранение доли АТС со скоростью 1 и 0.
def save_proportion(moved, not_moved, path):
    with open(path, "a") as file:
        file.write(str(moved) + " " + str(not_moved) + "\n")


# path - буть к .bin файлу.
def get_all_data(path):
    with shelve.open(path) as data:
        obj = [data[ob] for ob in data]
    return obj
