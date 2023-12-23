from turtle import color, width
import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
y_lim = 600
y_valid_min = 0

def upper(df):
    second_10_num = int(len(df)*0.1 - 1)
    limit_time = int(len(df)*0.15 - 1)
    tem = 0
    for i in range(second_10_num, limit_time, 1):
        if tem < df[i]:
            tem = df[i]
    return tem

get_time = 100
if __name__ == "__main__":
    fig, ax = plt.subplots()
    #ax.set_xlim(0, get_time)
    #ax.set_xlim(-50, 50)
    ax.set_xlim(-15, 15)
    ax.set_ylim(y_valid_min, y_lim)
    #plt.xticks([10, 70, 100])

    ax2 = ax.twinx()
    #ax2.set_ylim(y_valid_min, 60)
    ax2.set_ylim(y_valid_min, y_lim)
    #ax2.spines['right'].set_visible(False)
    #ax2.set_yticks([])
    #ax2.set_ylabel("max concentration level for 10 seconds [-]")

    #plt.xlabel("time [s]")
    #plt.xlabel("x_L [mm]")
    #ax.set_xlabel("x_L [mm]")
    #plt.xlabel("phi [degree]")
    ax.set_xlabel("phi [degree]")
    ax.set_ylabel("max concentration level for all time [-]")
    plt.title("Odor Source phi=6")
    #plt.title("Odor Source x_L=30")

    scatter_size = 200
    x = []
    y = []
    upper_t = []
    x_ticks = []
    for k in range(-12, 13, 6):
    #for k in range(-40, 41, 10):
        x_ticks.append(k)
        file_name = f"20231218-ex2-Ophi=6-all-phi={k}.csv"
        #file_name = f"20231218-ex1-x_O=30-x_L={k}.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        data_number = len(df)
        print(len(df))
        #first_value = df[]
        f = get_time / data_number#サンプリング周期[s]
        t = []
        for i in range(data_number):
            t.append(i*f)
        x.append(k)
        y.append(max(df))
        upper_t.append(upper(df))
        #plt.scatter(t, df, marker="o", label = f"x_L={k}", s=scatter_size)
        #plt.plot(t, df, label = f"x_L={k}")
    
    ax.bar(x, y, width = -2, align='edge', label = "max value for all time [-]")
    ax2.bar(x, upper_t, width = 2, align='edge', label = "max value for 5 seconds [-]", color = "green")
    """
    file_name = "aaa.csv"
    df = pd.read_csv(file_name, header=None)
    df = df.iloc[0:, 0].values
    data_number = len(df)
    f = get_time / data_number
    t = []
    for i in range(data_number):
        t.append(i*f)
    #plt.scatter(t, df, marker="o", label = f"x_L=40 non-directivity", s=scatter_size)
    #plt.scatter(40, max(df), marker="o", label = "without deaf", s=scatter_size)
    ax.scatter(40 - 1, max(df), marker="o", label = "max value without deaf [-]", s=scatter_size)
    ax2.scatter(40 + 1, upper(df), marker="o", label = "up time without deaf [s]", s=scatter_size, color = "red")
    #plt.plot(t, df, label = f"x_L=40 non-directivity")
    """
    
    plt.xticks(x_ticks)
    #plt.legend(loc="upper left", fontsize=17, ncol=5)
    ax.legend(loc="upper left", fontsize=17, ncol=5)
    ax2.legend(loc="upper right", fontsize=17, ncol=5)
    #plt.legend(loc="upper left", fontsize=17)

    ax.grid(True)
    ax2.grid(True)

    # グラフの表示
    plt.show()
