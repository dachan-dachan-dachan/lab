import matplotlib.pyplot as plt
import pandas as pd


def plot(csv_file_name, color, N_air, label):
    df = pd.read_csv(csv_file_name, header=None)
    df = df.iloc[:, 0].values
    data_number = len(df)
    f = get_time / data_number#サンプリング周期[s]
    t = []
    value = []
    for i in range(data_number):
        t.append(i*f)
        value.append(from_N_make_ppm(N_air, df[i]))
    plt.plot(t, value, marker="o", linestyle="", label = label, color=color)

#N_air = 252
y_lim = 1023
y_valid_min = 0
left_file_name = "l.csv"
right_file_name = "r.csv"
null_file_name = "n.csv"
get_time = 60*3
if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_xlim(0, get_time)
    ax.set_ylim(0, y_lim)

    plt.xlabel("time [s]")
    plt.ylabel("concentration level [-]")
    plt.title("Time Diagram")

    scatter_size = 3
    
    df = pd.read_csv(right_file_name)
    df = df.iloc[1:, 0].values
    data_number = len(df)
    f = get_time / data_number#サンプリング周期[s]
    t = []
    for i in range(data_number):
        t.append(i*f)
    plt.scatter(t, df, marker="o", linestyle="", label = "Right", color = "blue", s=scatter_size)
    
    df = pd.read_csv(left_file_name)
    df = df.iloc[1:, 0].values
    data_number = len(df)
    f = get_time / data_number#サンプリング周期[s]
    t = []
    for i in range(data_number):
        t.append(i*f)
    plt.scatter(t, df, marker="o", linestyle="", label = "Left", color = "red", s=scatter_size)

    df = pd.read_csv(null_file_name)
    df = df.iloc[1:, 0].values
    data_number = len(df)
    f = get_time / data_number#サンプリング周期[s]
    t = []
    for i in range(data_number):
        t.append(i*f)
    plt.scatter(t, df, marker="o", linestyle="", label = "Null", color = "green", s=scatter_size)
    
    plt.legend(loc="upper left")


    ax.grid(True)

    # グラフの表示
    plt.show()