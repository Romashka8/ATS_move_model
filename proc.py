from road_scripts import model_base as mb
import road_scripts.v as v
import time
import sys
import os

if __name__ == "__main__":
    # T_proc - for proc research.
    T_proc = 500
    r_size = 100
    # all ats in system for modeling.
    all_ats = int(sys.argv[1])
    # cluster или no_cluster(сам кластер включается/выключается в классе БАТС).
    cluster = sys.argv[2]
    # концентрация АТС в потоке(от 0.0 до 1.0).
    human_ats_concentration = float(sys.argv[3])
    try:
        os.mkdir(f"./res/proc/{human_ats_concentration}/")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"./res/proc/{human_ats_concentration}/{all_ats}/")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"./res/proc/{human_ats_concentration}/{all_ats}/{cluster}")
    except FileExistsError:
        pass
    start_time = time.time()
    h_arr, r_arr = mb.generate_arrays(all_ats, human_ats_concentration, 1, False)
    for i in range(1, T_proc):
        print(i)
        v.reset_v()
        mb.proc_do(h_arr, r_arr)
        v.v = v.v / (i * all_ats)
        moved_ats = sum(list(map(lambda x: x.moved, h_arr + r_arr)))
        mb.save_proportion(moved_ats, all_ats - moved_ats,
                           f"res/proc/{human_ats_concentration}/{all_ats}/{cluster}/{all_ats}(prop).txt")
        mb.proc_reset(h_arr, r_arr)
        mb.save_stat(float(i), v.v, f"res/proc/{human_ats_concentration}/{all_ats}/{cluster}/{all_ats}.txt")
