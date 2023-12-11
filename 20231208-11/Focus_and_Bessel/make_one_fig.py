import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
y_valid_min = 0
file_name = "20231210-z_S=400-z_F=150.csv"
if __name__ == "__main__":
    fig, ax = plt.subplots()

    plt.xlabel("time [s]")
    plt.ylabel("concentration level [-]")
    plt.title("Time Diagram")
    
    y_value = []
    get_time = []

    df = pd.read_csv(file_name)
    df = df.iloc[1:, 0].values
    for i in range(len(df)):
        y_value.append(df[i])
    get_time = 30+90+90
    """
    del y_value[0]
    del y_value[0]
    del y_value[0]
    """
    #del y_value[-1]

    sum_time = 30 + 90 + 90
    ax.set_xlim(0, sum_time)
    ax.set_ylim(0, y_lim)
    
    data_number = len(y_value)
    f = sum_time / data_number#サンプリング周期[s]
    t = []
    for i in range(data_number):
        t.append(i*f)

    plt.scatter(t, y_value, marker="o", linestyle="", color = "red", s = 2)
    plt.legend(title = "Focus=150[mm]", loc="upper left")

    #ax.set_xticks([30,60,90,120,150,180,210])
    ax.set_xticks([30,120,210])
    ax.grid(True)

    # グラフの表示
    plt.show()
