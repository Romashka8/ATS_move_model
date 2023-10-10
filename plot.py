import matplotlib.pyplot as plt


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
    plt.plot(x, y, label=f"R(HDV) = {hdv}", color=color)


# cluster or no_cluster
folder = "res/cluster/"

data1 = read_data(f"{folder}00/1_1000.txt")
data2 = read_data(f"{folder}01/1_1000.txt")
data3 = read_data(f"{folder}03/1_1000.txt")
data4 = read_data(f"{folder}07/1_1000.txt")
data5 = read_data(f"{folder}10/1_1000.txt")

make_plot(data1, 0.0, "black")
make_plot(data2, 0.1, "red")
make_plot(data3, 0.3, "green")
make_plot(data4, 0.7, "blue")
make_plot(data5, 1.0, "purple")

plt.title("Рисунок 6(б)")
plt.xlabel("p [число АТС на ячейку]")
plt.ylabel("q [число АТС в еденицу времени]")
plt.ylim(0, 1)
plt.legend()
plt.show()
