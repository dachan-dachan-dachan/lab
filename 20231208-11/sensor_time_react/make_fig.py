import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
y_valid_min = 0
first_csv_file_name = "l.csv"
second_csv_file_name = "l.csv"
third_csv_file_name = "l.csv"
get_time = 180
label = "left"
color = "blue"
if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_xlim(0, get_time)
    ax.set_ylim(0, y_lim)

    plt.xlabel("time [s]")
    plt.ylabel("concentration level [-]")
    plt.title("Time Diagram")
    
    #df = pd.read_csv(csv_file_name, header=None)
    df = pd.read_csv(csv_file_name)
    df = df.iloc[1:, 0].values
    data_number = len(df)
    f = get_time / data_number#サンプリング周期[s]
    t = []
    for i in range(data_number):
        t.append(i*f)
    plt.plot(t, df, marker="o", linestyle="", label = label, color = color)
    plt.legend(loc="upper left")

    ax.grid(True)

    # グラフの表示
    plt.show()
