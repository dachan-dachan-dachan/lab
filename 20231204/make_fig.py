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


#N_air = 252
y_lim = 5000
y_valid_min = 50
#csv_file = "data.csv"
if __name__ == "__main__":
    N_air = float(input("空気中の10bitの数値を入力："))
    csv_file_number = int(input("読み込みたいcsvファイルの数を入力："))
    csv_file_name = []
    date_name = []
    for i in range(csv_file_number):
        temp = input(f"{i+1}個目のcsvファイルの名前を入力：")
        csv_file_name.append(temp)
        temp = input(f"{i+1}個目のcsvファイルの凡例を入力：")
        date_name.append(temp)
    get_time = float(input("サンプルに要した時間[s]を入力："))
    y_scale = int(input("線形軸→0，対数軸→1："))
    
    for i in range(csv_file_number):
        df = pd.read_csv(csv_file_name[i], header=None)
        df = df.iloc[:, 0].values
        data_number = len(df)
        f = get_time / data_number#サンプリング周期[s]
        t = []
        value = []
        for j in range(data_number):
            t.append(j*f)
            value.append(from_N_make_ppm(N_air, df[j]))
            plt.plot(t, value, marker="o", linestyle="", label = date_name[i], color ="blue")
    

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

    plt.xlabel("time [s]")
    plt.ylabel("concentration [ppm]")
    plt.title("ppm-t")
    
    plt.plot([0, get_time], [y_valid_min, y_valid_min], linestyle="--", label="lowest valid value", color="red")
    
    plt.legend(loc="upper left")

    ax.grid(True)

    # グラフの表示
    plt.show()
