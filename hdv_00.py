from road_scripts import model_base as mb
from road_scripts.road import roads
from ats_scripts.robot_ats import RobotATS
import road_scripts.v as v
import time
import sys


if __name__ == "__main__":
    # дописать значение в 0 в файл.
    start = int(sys.argv[1])
    finish = int(sys.argv[2])
    # stat or stab.
    mode = sys.argv[3]
    # cluster or no_cluster.
    cluster = sys.argv[4]
    if mode == "stab":
        input()
        start_time = time.time()
        for i in range(start, finish + 1):
            print(i)
            h_arr, r_arr = mb.generate_arrays(i, 0, 0)
            mb.rec_stab(4000, h_arr, r_arr)
            RobotATS.delayed = []
            mb.save_conf(f"{i}", f"res/{cluster}/00/{start}_{finish}.bin", roads[0], h_arr, r_arr)
            roads[0].clear_road()
    if mode == "stat":
        input()
        start_time = time.time()
        for i in range(start, finish + 1):
            print(i)
            v.reset_v()
            rm, h_arr, r_arr = mb.load_conf(f"{i}", f"res/{cluster}/00/{start}_{finish}.bin")
            roads[0] = rm
            RobotATS.delayed = []
            mb.rec_stat(5000, h_arr, r_arr)
            v.v = v.v / (5000 * i)
            mb.save_stat(i / 1000, v.v, f"res/{cluster}/00/{start}_{finish}.txt")
    print(time.time() - start_time)
