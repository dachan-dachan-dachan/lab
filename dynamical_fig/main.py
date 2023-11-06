#実行方法：cmd：streamlit run main.py

import streamlit as st
import pandas as pd
import csv
import time
import plotly.express as px

#import sys
import serial
#import datetime


def get_date(csv_file, port_ad, port_num):#https://qiita.com/ryota765/items/0cfc2ea2d598de11b174
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
    value = float(ser.readline().decode("UTF-8").rstrip("\n"))
#    print(value)
#    with open(csv_file, "a") as fi:
#        print("{}".format(value), file=fi)
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([value])


def fig(csv_file, f, placeholder):
    y_a = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            y_a.append(float(row[0]))
    x_a = [i * f for i in range(len(y_a))]
    fig = px.line(x=x_a, y=y_a, title='アナログ電圧のリアルタイム表示')
    fig.update_xaxes(title_text='時間 [s]')
    fig.update_yaxes(title_text='電圧 [V]')
    placeholder.write(fig)


def main_code(port_ad, port_num, csv_file, f):
    placeholder = st.empty()
    while True:
        get_date(csv_file, port_ad, port_num)
        fig(csv_file, f, placeholder)
        time.sleep(f)


f = 0.001#サンプリング周期 [s]
port_ad = "/dev/cu.usbmodem14101"
port_num = 9600
csv_file = 'voltage.csv'

if __name__ == '__main__':
    main_code(port_ad, csv_file, f)
