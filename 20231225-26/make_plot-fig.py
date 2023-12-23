import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
y_valid_min = 0

get_time = 100
if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_xlim(0, get_time)
    ax.set_ylim(y_valid_min, y_lim)
    plt.xticks([10, 70, 100])

    plt.xlabel("time [s]")
    plt.ylabel("concentration level [-]")
    plt.title("Odor Source x_L=30")

    scatter_size = 3
    
    for k in range(-40, 50, 10):
        file_name = f"20231224-phi={k}_0.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        data_number = len(df)
        f = get_time / data_number#サンプリング周期[s]
        t = []
        for i in range(data_number):
            t.append(i*f)
        plt.scatter(t, df, marker="o", label = f"phi={k} with", s=scatter_size)

    for k in range(-40, 50, 10):
        file_name = f"20231224-phi={k}_1.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        data_number = len(df)
        f = get_time / data_number#サンプリング周期[s]
        t = []
        for i in range(data_number):
            t.append(i*f)
        plt.scatter(t, df, marker="o", label = f"phi={k} without", s=scatter_size)
    

    #plt.legend(loc="upper left", fontsize=17, ncol=2)
    plt.legend(loc="upper left", fontsize=17)

    ax.grid(True)

    # グラフの表示
    plt.show()
