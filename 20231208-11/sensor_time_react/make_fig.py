import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
y_valid_min = 0
first_csv_file_name = "20231208_react_time_1.csv"
second_csv_file_name = "20231208_react_time_2.csv"
third_csv_file_name = "20231208_react_time_3.csv"
if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_xlim(0, get_time)
    ax.set_ylim(0, y_lim)

    plt.xlabel("time [s]")
    plt.ylabel("concentration level [-]")
    plt.title("Time Diagram")
    
    y_value = []
    get_time = []

    df = pd.read_csv(first_csv_file_name, header=None)
    df = df.iloc[1:, 0].values
    y_value.append(df)
    get_time.append(df[-1])
    del y_value[-1]

    df = pd.read_csv(second_csv_file_name, header=None)
    df = df.iloc[1:, 0].values
    y_value.append(df)
    get_time.append(df[-1])
    del y_value[-1]

    df = pd.read_csv(third_csv_file_name, header=None)
    df = df.iloc[1:, 0].values
    y_value.append(df)
    get_time.append(df[-1])
    del y_value[-1]

    
    data_number = len(y_value[0]) + len(y_value[1]) + len(y_value[2])
    f = (get_time[0] + get_time[1] + get_time[2]) / data_number#サンプリング周期[s]
    t = []
    t.append([])
    t.append([])
    t.append([])
    for i in range(data_number):
        if i*f <= get_time[0]:
            t[0].append(i*f)
        elif i*f <= get_time[1]:
            t[1].append(i*f)
        elif i*f <= get_time[2]:
            t[2].append(i*f)

    """
    plt.scatter(t[0:len(y_value[0])], y_value[0], marker="o", linestyle="", label = "OFF", color = "red", s = 2)
    plt.scatter(t[len(y_value[0]):len(y_value[1])], y_value[1], marker="o", linestyle="", label = "ON", color = "blue", s = 2)
    plt.scatter(t[len(y_value[1]):len(y_value[2])], y_value[2], marker="o", linestyle="", color = "red", s = 2)
    """
    plt.scatter(t[0], y_value[0], marker="o", linestyle="", label = "OFF", color = "red", s = 2)
    plt.scatter(t[1], y_value[1], marker="o", linestyle="", label = "ON", color = "blue", s = 2)
    plt.scatter(t[2], y_value[2], marker="o", linestyle="", color = "red", s = 2)
    
    plt.legend(loc="upper left")

    ax.grid(True)

    # グラフの表示
    plt.show()
