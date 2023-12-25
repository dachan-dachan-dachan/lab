from turtle import color, width
import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
#y_lim = 600
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
    #ax.set_xlim(-15, 15)
    ax.set_ylim(y_valid_min, y_lim)
    #plt.xticks([10, 70, 100])

    ax2 = ax.twinx()
    ax2.set_ylim(y_valid_min, y_lim)

    ax.set_xlabel("phi [degree]")
    ax.set_ylabel("max concentration level [-]")
    plt.title("Odor Source phi=6")

    scatter_size = 200
    x = []
    y = []
    upper_t = []
    x_ticks = []
    for k in range(-12, 13, 6):
        x_ticks.append(k)
        file_name = f"20231224-phi={k}_0.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        data_number = len(df)
        x.append(k)
        y.append(max(df))
    ax.bar(x, y, width = -2, align = "edge", label = "max value with [-]", color = "blue")

    for k in range(-12, 13, 6):
        #x_ticks.append(k)
        file_name = f"20231224-phi={k}_1.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        data_number = len(df)
        x.append(k)
        y.append(max(df))
    ax2.bar(x, upper_t, width = 2, align = "edge", label = "max value without [-]", color = "red")

    file_name = "20231224_1.csv"
    df = pd.read_csv(file_name, header=None)
    df = df.iloc[0:, 0].values
    x = [-50, 50]
    y = [max(df), max(df)]
    ax3 = ax.twinx()
    ax3.set_ylim(y_valid_min, y_lim)
    ax3.plot(x, y, label = "max value only [-]", marker = "", linestyle = "-", color = "green")
    
    
    plt.xticks(x_ticks)
    #plt.legend(loc="upper left", fontsize=17, ncol=5)
    ax.legend(loc="upper left", fontsize=17, ncol=5)
    ax2.legend(loc="upper right", fontsize=17, ncol=5)
    #plt.legend(loc="upper left", fontsize=17)

    ax.grid(True)
    ax2.grid(True)

    ax3.legend(loc="upper center", fontsize=17, ncol=5)
    ax3.grid(True)

    # グラフの表示
    plt.show()
