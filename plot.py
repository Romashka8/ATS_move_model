import matplotlib.pyplot as plt
import scipy.signal


def read_data(path):
    data = []
    with open(path, "r") as file:
        for i in file.readlines():
            row = list(map(float, i[1:].split(" ")))
            data.append(row)
    return data


def make_plot(data, hdv, color):
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    # y = [i / 1000 for i in range(0, 100, 10)] + y[10:]
    # print(y)
    # y = scipy.signal.savgol_filter(y, len(y), 3)
    plt.plot(x, y, label=f"R(HDV) = {hdv}", color=color)


folder = "res/no_cluster/"

data1 = read_data(f"{folder}00/1_100.txt")
data2 = read_data(f"{folder}01/1_100.txt")
data3 = read_data(f"{folder}03/1_100.txt")
data4 = read_data(f"{folder}07/1_100.txt")
data5 = read_data(f"{folder}10/1_100.txt")

make_plot(data1, 0.0, "black")
make_plot(data2, 0.1, "red")
make_plot(data3, 0.3, "green")
make_plot(data4, 0.7, "blue")
make_plot(data5, 1.0, "purple")

plt.title("Рисунок 6(а)")
plt.xlabel("p [число АТС на ячейку]")
plt.ylabel("q [число АТС в еденицу времени]")
plt.ylim(0, 1)
plt.legend()
plt.show()
