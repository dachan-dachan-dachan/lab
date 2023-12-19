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
        file_name = f"20231218-ex1-x_O=30-x_L={k}.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        data_number = len(df)
        f = get_time / data_number#サンプリング周期[s]
        t = []
        for i in range(data_number):
            t.append(i*f)
        plt.scatter(t, df, marker="o", label = f"x_L={k}", s=scatter_size)
    

    
    file_name = "aaa.csv"
    df = pd.read_csv(file_name, header=None)
    df = df.iloc[0:, 0].values
    data_number = len(df)
    f = get_time / data_number
    t = []
    for i in range(data_number):
        t.append(i*f)
    plt.scatter(t, df, marker="o", label = f"x_L=40_non-directivity", s=scatter_size)
    

    plt.legend(loc="upper left")


    ax.grid(True)

    # グラフの表示
    plt.show()
