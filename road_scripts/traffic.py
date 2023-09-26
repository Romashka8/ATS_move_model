# вспомогательный модуль для генерации траффика.
# основная цель - упорядочивать АТС на дороге.
from ats_scripts.robot_ats import RobotATS
import numpy as np


def insert_sort(arr):
    for i in range(len(arr)):
        j = i - 1
        key = arr[i]
        while arr[j].position > key.position and j >= 0:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def check_head(r_ats_array):
    try:
        if r_ats_array[0].position == 0 and RobotATS.cluster:
            return r_ats_array[1:] + [r_ats_array[0]]
        if r_ats_array[-1].position == 0:
            return [r_ats_array[-1]] + r_ats_array[:-1]
        return r_ats_array
    except IndexError:
        return r_ats_array


def generate_r_ats(r_ats_count, rm, key):
    r_ats = [RobotATS(np.random.choice(rm.get_free_cells()), rm, key) for i in range(r_ats_count)]
    r_ats = insert_sort(r_ats)
    # return r_ats[::-1] if RobotATS.cluster else r_ats
    return r_ats
