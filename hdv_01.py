from road_scripts import model_base as mb
from road_scripts.road import roads
from ats_scripts.robot_ats import RobotATS
import road_scripts.v as v
import time
import sys

if __name__ == "__main__":
    # T_s, T_e, r_size, research - for basic and break research.
    T_s = 4000
    T_e = 5000
    r_size = 1000
    # all ats in system for modeling.
    start = int(sys.argv[1])
    finish = int(sys.argv[2])
    # stat or stab.
    mode = sys.argv[3]
    # cluster or no_cluster.
    cluster = sys.argv[4]
    # base or break.
    research = sys.argv[5]
    if mode == "stab":
        input()
        start_time = time.time()
        for i in range(start, finish + 1):
            print(i)
            h_arr, r_arr = mb.generate_arrays(i, 0.1, 1, False)
            mb.rec_stab(T_s, h_arr, r_arr)
            RobotATS.delayed = []
            mb.save_conf(f"{i}", f"res{research}/{cluster}/01/{start}_{finish}.bin", roads[1], h_arr, r_arr)
            roads[1].clear_road()
    if mode == "stat":
        input()
        start_time = time.time()
        for i in range(start, finish + 1):
            print(i)
            v.reset_v()
            rm, h_arr, r_arr = mb.load_conf(f"{i}", f"res{research}/{cluster}/01/{start}_{finish}.bin")
            roads[1] = rm
            RobotATS.delayed = []
            mb.rec_stat(T_e, h_arr, r_arr)
            v.v = v.v / (T_e * i)
            mb.save_stat(i / r_size, v.v, f"res{research}/{cluster}/01/{start}_{finish}.txt")
    print(time.time() - start_time)
