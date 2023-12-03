import matplotlib.pyplot as plt
import pandas as pd


def from_N_make_ppm(N_air, N_alc):
    R = 20.7*(((1023/N_alc)-1)/((1023/N_air)-1))
    if R == 0:
        return None
    else:
        if R > 101*(100**(-0.85)):
            return (101/R)**(1/0.85)
        else:
            return (35/R)**(1/0.62)

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
y_lim = 5000
y_valid_min = 50
#csv_file = "data.csv"
get_time = 600
if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_xlim(0, get_time)
    ax.set_ylim(0, y_lim)

    plt.xlabel("time [s]")
    plt.ylabel("concentration [ppm]")
    plt.title("ppm-t")
    
    N_air = float(input("空気中のセンサの出力値："))
    file_num = int(input("読み込むcsvファイルの個数を入力："))
    for i in range(file_num):
        csv_file_name = input(f"{i+1}個目のcsvファイル名：")
        label = input(f"{i+1}個目のラベル名：")
        if i % 4 == 0:
            point_color = "blue"
        elif i % 4 == 1:
            point_color = "green"
        elif i % 4 == 2:
            point_color = "yellow"
        elif i % 4 == 3:
            point_color = "magenta"
        plot(csv_file_name, point_color, N_air, label)
    plt.plot([0, get_time], [y_valid_min, y_valid_min], linestyle="--", label="lowest valid value", color="red")
    
    plt.legend(loc="upper left")

    ax.grid(True)

    # グラフの表示
    plt.show()
