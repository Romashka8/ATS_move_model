import matplotlib.pyplot as plt


all_ats_list = [25, 50, 75, 90]
concentrate = "1.0"
cluster = "no_cluster"



def read_data(path):
    data = []
    with open(path, "r") as file:
        for i in file.readlines():
            row = list(map(float, i.split(" ")))
            data.append(row)
    return data


def make_plot(data, all_ats, color):
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    plt.plot(x, y, label=f"Число АТС в системе = {all_ats}", color=color)


def make_prop(data):
    x = [i for i in range(len(data))]
    y1 = [i[0] for i in data]
    y2 = [i[1] for i in data]
    plt.scatter(x, y1, label="Переместившиеся АТС", color="green")
    plt.scatter(x, y2, label="Не переместившееся АТС", color="red")


def proc_plots():
    # 0.1 - концентрация АТС, 25,50,75,90 - общее число АТС в системе.
    data1 = read_data(f"res/proc/{concentrate}/{all_ats_list[0]}/{cluster}/{all_ats_list[0]}.txt")
    data2 = read_data(f"res/proc/{concentrate}/{all_ats_list[1]}/{cluster}/{all_ats_list[1]}.txt")
    data3 = read_data(f"res/proc/{concentrate}/{all_ats_list[2]}/{cluster}/{all_ats_list[2]}.txt")
    data4 = read_data(f"res/proc/{concentrate}/{all_ats_list[3]}/{cluster}/{all_ats_list[3]}.txt")
    make_plot(data1, all_ats_list[0], "black")
    make_plot(data2, all_ats_list[1], "red")
    make_plot(data3, all_ats_list[2], "green")
    make_plot(data4, all_ats_list[3], "blue")
    plt.title("Разброс переместившихся АТС от времени моделирования(без БАТС)(90 АТС).")
    plt.xlabel("t [время, прошедшее с начала моделирования]")
    plt.ylabel("k [колличество переместившихся АТС]")
    plt.legend()
    plt.show()


def scat_plot():
    data = read_data(f"res/proc/{concentrate}/{all_ats_list[0]}/{cluster}/{all_ats_list[0]}(prop).txt")
    make_prop(data)
    plt.title("Разброс переместившихся АТС от времени моделирования(без БАТС)(25 АТС).")
    plt.xlabel("t [время, прошедшее с начала моделирования]")
    plt.ylabel("k [колличество переместившихся АТС]")
    plt.legend()
    plt.show()


# proc_plots()

scat_plot()
