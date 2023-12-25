from turtle import color, width
import matplotlib.pyplot as plt
import pandas as pd


y_lim = 1023
y_lim = 300
y_valid_min = 0

def upper(df):
    second_10_num = int(len(df)*0.1 - 1)
    limit_time = int(len(df)*0.15 - 1)
    tem = 0
    for i in range(second_10_num, limit_time, 1):
        if tem < df[i]:
            tem = df[i]
    return tem

get_time = 60
if __name__ == "__main__":
    fig, ax = plt.subplots()
    plt.xlim(-20, 20)
    plt.ylim(y_valid_min, y_lim)
    plt.xticks([-10,0,10])
    plt.xlabel("phi [degree]")
    plt.ylabel("max concentration level [-]")
    plt.title("Odor Source phi=10")

    scatter_size = 200
    x = []
    y = []
    for k in range(-10, 11, 10):
        file_name = f"20231225_theat={k}_with.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        x.append(k)
        y.append(max(df))
    plt.bar(x, y, width = -2, align = "edge", label = "max value with [-]", color = "blue")

    x = []
    y = []
    for k in range(-10, 11, 10):
        file_name = f"20231225_theat={k}_without.csv"
        df = pd.read_csv(file_name, header=None)
        df = df.iloc[0:, 0].values
        x.append(k)
        y.append(max(df))
    plt.bar(x, y, width = 2, align = "edge", label = "max value without [-]", color = "red")

    
    file_name = "20231225_only.csv"
    df = pd.read_csv(file_name, header=None)
    df = df.iloc[0:, 0].values
    x = [-50, 50]
    y = [max(df), max(df)]
    plt.plot(x, y, label = "max value only [-]", marker = "", linestyle = "--", linewidth = 3, color = "green")
    
    
    plt.legend(loc="upper left", fontsize=17, ncol=5)
    plt.grid()
    #plt.legend(loc="upper left", fontsize=17)


    # グラフの表示
    plt.show()
