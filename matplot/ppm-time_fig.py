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


N_air = 252
y_lim = 5000
y_valid_min = 50
csv_file = "data.csv"
if __name__ == "__main__":
    get_time = float(input("サンプルに要した時間[s]を入力："))
    y_scale = int(input("線形軸→0，対数軸→1："))
    df = pd.read_csv(csv_file, header=None)
    df = df.iloc[:, 0].values
    data_number = len(df)
    f = get_time / data_number#サンプリング周期[s]
    t = []
    value = []
    for i in range(data_number):
        t.append(i*f)
        value.append(from_N_make_ppm(N_air, df[i]))
    
    max_value = max(value)

    fig, ax = plt.subplots()
    ax.set_xlim(0, get_time)
    if y_scale == 1:
        base = float(input("対数の底を入力："))
        plt.yscale("log", base=base)
        ax.set_ylim(10, 10000)
    elif y_scale == 0:
        y_flag = int(input("y軸の上限を固定する→0，しない→1："))
        if y_flag == 0:
            ax.set_ylim(0, y_lim)
        elif y_flag == 1:
            ax.set_ylim(0, max_value + 1000)
            if max_value > y_lim:
                plt.plot([0, get_time], [y_lim, y_lim], linestyle="--", label="max valid value", color="red")

    plt.xlabel("time [s]")
    plt.ylabel("concentration [ppm]")
    plt.title("ppm-t")

    plt.plot(t, value, marker="o", linestyle="", label="concentration", color ="blue")
    plt.plot([0, get_time], [y_valid_min, y_valid_min], linestyle="--", label="lowest valid value", color="red")
    
    title_position = plt.gca().title.get_position()
    plt.text(title_position[0] + 0.2, title_position[1] + 0.05, f"max value = {max_value:.1f} [ppm]\nminimum value = {min(value):.1f} [ppm]", color="black", transform=plt.gca().transAxes)

    plt.legend(loc="upper left")

    ax.grid(True)

    # グラフの表示
    plt.show()
