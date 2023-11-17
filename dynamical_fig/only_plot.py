import matplotlib.pyplot as plt
import numpy as np
import matplotlib

import serial
import csv
import plotly.express as px

def get_date(csv_file, port_ad, port_num):#参考：https://qiita.com/ryota765/items/0cfc2ea2d598de11b174
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
    value = int(ser.readline().decode("UTF-8").rstrip("\n"))
    volt = round(5*value/1023,2)#5/(2^10 -1)=0.00449より有効桁数は小数第2位で設定
#    print(volt)
#    with open(csv_file, "a") as fi:
#        print("{}".format(volt), file=fi)
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([volt])


def read_date(csv_file, f):
    y = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            y.append(float(row[0]))
    x = [i * f for i in range(len(y))]
    return x, y


def main_code(csv_file, port_ad, port_num, f):
    fig, ax = plt.subplots(1, 1)# 描画領域を取得
    ax.set_ylim((0, 5))# y軸方向の描画幅を指定
    while True:
        get_date(csv_file, port_ad, port_num)
        x, y = read_date(csv_file, f)

        line, = ax.plot(x, y, color='blue')# グラフを描画する
        plt.pause(f)# 次の描画までf秒待つ
        line.remove()# グラフをクリア



f = 0.001
csv_file = 'voltage.csv'
port_ad = "/dev/cu.usbmodem14101"
port_num = 9600

if __name__ == '__main__':
    main_code(csv_file, port_ad, port_num, f)
